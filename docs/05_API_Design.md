# API Design Document

## Project Name

**DataDoctor AI**

---

# 1. Overview

This document defines the API architecture and endpoint specifications for DataDoctor AI.

Although the MVP will initially use Django Templates for the frontend, all business functionality will be exposed through internal REST APIs.

This approach ensures future support for:

* React Frontend
* Vue Frontend
* Mobile Applications
* Third-Party Integrations
* Public API Access

---

# 2. API Design Principles

The API must follow these principles:

## Consistency

All endpoints should follow consistent naming conventions.

---

## Security

All authenticated endpoints require a valid user session or authentication token.

---

## Versioning

All APIs will be versioned.

Example:

```text
/api/v1/
```

This allows future versions without breaking existing integrations.

---

## Resource-Oriented Design

Endpoints represent business resources.

Examples:

```text
/users/
/datasets/
/profiles/
/reports/
```

---

# 3. Base URL Structure

```text
/api/v1/
```

Example:

```text
/api/v1/datasets/
```

---

# 4. Authentication APIs

## Register User

### Endpoint

```http
POST /api/v1/auth/register/
```

### Request

```json
{
  "username": "johnsmith",
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```

### Response

```json
{
  "success": true,
  "message": "User registered successfully."
}
```

---

## Login User

### Endpoint

```http
POST /api/v1/auth/login/
```

### Request

```json
{
  "username": "johnsmith",
  "password": "SecurePassword123!"
}
```

### Response

```json
{
  "success": true,
  "message": "Login successful."
}
```

---

## Logout User

### Endpoint

```http
POST /api/v1/auth/logout/
```

### Response

```json
{
  "success": true,
  "message": "Logout successful."
}
```

---

# 5. Dataset APIs

## Upload Dataset

### Endpoint

```http
POST /api/v1/datasets/upload/
```

### Content Type

```text
multipart/form-data
```

### Request

```text
file=sales_data.xlsx
```

### Response

```json
{
  "success": true,
  "dataset_id": "uuid",
  "status": "UPLOADED"
}
```

---

## List User Datasets

### Endpoint

```http
GET /api/v1/datasets/
```

### Response

```json
{
  "count": 2,
  "results": [
    {
      "id": "uuid",
      "name": "Sales Data",
      "status": "PROFILED"
    }
  ]
}
```

---

## Dataset Details

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/
```

### Response

```json
{
  "id": "uuid",
  "name": "Sales Data",
  "file_type": "xlsx",
  "status": "PROFILED",
  "uploaded_at": "2026-06-15T12:00:00Z"
}
```

---

## Delete Dataset

### Endpoint

```http
DELETE /api/v1/datasets/{dataset_id}/
```

### Response

```json
{
  "success": true,
  "message": "Dataset deleted successfully."
}
```

---

# 6. Profiling APIs

## Generate Dataset Profile

### Endpoint

```http
POST /api/v1/datasets/{dataset_id}/profile/
```

### Response

```json
{
  "success": true,
  "status": "PROFILING"
}
```

---

## Get Dataset Profile

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/profile/
```

### Response

```json
{
  "row_count": 5000,
  "column_count": 15,
  "duplicate_rows": 24,
  "missing_values": {
    "email": 15,
    "revenue": 7
  }
}
```

---

# 7. Quality Assessment APIs

## Generate Quality Score

### Endpoint

```http
POST /api/v1/datasets/{dataset_id}/quality/
```

### Response

```json
{
  "success": true
}
```

---

## Get Quality Score

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/quality/
```

### Response

```json
{
  "completeness_score": 92.5,
  "consistency_score": 89.4,
  "validity_score": 95.0,
  "uniqueness_score": 100.0,
  "overall_score": 94.2
}
```

---

# 8. Cleaning Recommendation APIs

## Get Cleaning Recommendations

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/recommendations/
```

### Response

```json
{
  "recommendations": [
    {
      "column": "revenue",
      "issue": "missing_values",
      "recommended_action": "median"
    },
    {
      "column": "customer_name",
      "issue": "inconsistent_text",
      "recommended_action": "title_case"
    }
  ]
}
```

---

# 9. Cleaning APIs

## Execute Cleaning

### Endpoint

```http
POST /api/v1/datasets/{dataset_id}/clean/
```

### Request

```json
{
  "actions": [
    {
      "column": "revenue",
      "action": "median"
    },
    {
      "column": "customer_name",
      "action": "title_case"
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "job_id": "uuid",
  "status": "RUNNING"
}
```

---

## Cleaning Job Status

### Endpoint

```http
GET /api/v1/cleaning-jobs/{job_id}/
```

### Response

```json
{
  "job_id": "uuid",
  "status": "COMPLETED"
}
```

---

## Cleaning Summary

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/cleaning-summary/
```

### Response

```json
{
  "duplicates_removed": 24,
  "missing_values_fixed": 22,
  "dates_standardized": 18
}
```

---

# 10. Download APIs

## Download Cleaned CSV

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/download/csv/
```

### Response

File Download

```text
sales_data_cleaned.csv
```

---

## Download Cleaned Excel

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/download/xlsx/
```

### Response

File Download

```text
sales_data_cleaned.xlsx
```

---

# 11. Reporting APIs

## Generate Reports

### Endpoint

```http
POST /api/v1/datasets/{dataset_id}/reports/
```

### Response

```json
{
  "success": true
}
```

---

## List Reports

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/reports/
```

### Response

```json
{
  "reports": [
    {
      "id": "uuid",
      "type": "PDF"
    },
    {
      "id": "uuid",
      "type": "EXCEL"
    }
  ]
}
```

---

## Download Report

### Endpoint

```http
GET /api/v1/reports/{report_id}/download/
```

### Response

File Download

```text
quality_report.pdf
```

---

# 12. Dataset Status API

## Get Dataset Status

### Endpoint

```http
GET /api/v1/datasets/{dataset_id}/status/
```

### Response

```json
{
  "status": "PROFILED"
}
```

---

# 13. Status Definitions

## Dataset Statuses

```text
UPLOADED
PROFILING
PROFILED
REVIEW_PENDING
CLEANING
COMPLETED
FAILED
```

---

## Cleaning Job Statuses

```text
PENDING
RUNNING
COMPLETED
FAILED
```

---

# 14. Standard Success Response

All successful responses should follow a consistent structure.

```json
{
  "success": true,
  "message": "Operation completed successfully."
}
```

---

# 15. Standard Error Response

All errors should follow a consistent structure.

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid file format."
  }
}
```

---

# 16. HTTP Status Codes

| Status Code | Meaning               |
| ----------- | --------------------- |
| 200         | Success               |
| 201         | Created               |
| 400         | Bad Request           |
| 401         | Unauthorized          |
| 403         | Forbidden             |
| 404         | Not Found             |
| 500         | Internal Server Error |

---

# 17. Security Requirements

Authenticated endpoints require:

* Logged-in user
* Valid session
* CSRF protection

Users must only access their own datasets and reports.

---

# 18. Future API Enhancements

Version 2:

* Dataset comparison APIs
* User profile APIs

Version 3:

* Team workspace APIs
* Shared dataset APIs

Version 4:

* AI recommendation APIs
* Public developer APIs

---

# 19. API Approval

This document serves as the official API specification for DataDoctor AI MVP and will guide backend development, frontend integration, testing, and future platform expansion.
