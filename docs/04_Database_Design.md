# Database Design Document

## Project Name

**DataDoctor AI**

---

# 1. Overview

This document defines the database architecture for DataDoctor AI.

The database is designed to support:

* User authentication
* Dataset ownership
* Dataset versioning
* Profiling results
* Data quality assessments
* Cleaning operations
* Report generation
* Future SaaS scalability

Database Engine:

PostgreSQL

---

# 2. Database Design Principles

The database design follows the following principles:

## Data Integrity

Relationships must be enforced using foreign keys.

---

## Auditability

Original datasets must never be modified.

All cleaning operations should be traceable.

---

## Scalability

The design should support future features without major redesign.

Examples:

* Team workspaces
* Subscription plans
* Dataset sharing
* API integrations

---

## Performance

Indexes should be applied to frequently queried fields.

---

# 3. Entity Relationship Overview

```text
User
 |
 +---- Dataset
          |
          +---- DatasetVersion
          |
          +---- DatasetProfile
          |
          +---- QualityScore
          |
          +---- CleaningJob
          |
          +---- Report
```

---

# 4. Users Table

Uses Django's built-in authentication model.

Table:

auth_user

Primary Key:

id

---

## Purpose

Stores:

* User accounts
* Authentication details
* Account ownership

---

# 5. Dataset Table

Table Name:

datasets

---

## Purpose

Stores information about uploaded datasets.

---

### Fields

| Field         | Type         | Description        |
| ------------- | ------------ | ------------------ |
| id            | UUID         | Primary Key        |
| user_id       | FK           | Owner              |
| name          | VARCHAR(255) | Dataset Name       |
| original_file | VARCHAR(500) | Original File Path |
| file_type     | VARCHAR(20)  | CSV/XLSX           |
| file_size     | BIGINT       | File Size          |
| status        | VARCHAR(50)  | Processing Status  |
| uploaded_at   | TIMESTAMP    | Upload Date        |
| updated_at    | TIMESTAMP    | Last Update        |

---

## Indexes

```sql
INDEX(user_id)
INDEX(status)
INDEX(uploaded_at)
```

---

# 6. Dataset Version Table

Table Name:

dataset_versions

---

## Purpose

Tracks every dataset version.

Original and cleaned files are stored separately.

---

### Fields

| Field          | Type         | Description      |
| -------------- | ------------ | ---------------- |
| id             | UUID         | Primary Key      |
| dataset_id     | FK           | Dataset          |
| version_number | INTEGER      | Version Number   |
| file_path      | VARCHAR(500) | File Location    |
| version_type   | VARCHAR(50)  | ORIGINAL/CLEANED |
| created_at     | TIMESTAMP    | Creation Date    |

---

## Example

```text
Dataset
   |
   +---- Version 1 (Original)
   |
   +---- Version 2 (Cleaned)
```

---

# 7. Dataset Profile Table

Table Name:

dataset_profiles

---

## Purpose

Stores profiling results generated from uploaded datasets.

---

### Fields

| Field                | Type      | Description           |
| -------------------- | --------- | --------------------- |
| id                   | UUID      | Primary Key           |
| dataset_id           | FK        | Dataset               |
| row_count            | INTEGER   | Total Rows            |
| column_count         | INTEGER   | Total Columns         |
| missing_values       | JSONB     | Missing Value Summary |
| duplicate_rows       | INTEGER   | Duplicate Count       |
| unique_value_summary | JSONB     | Uniqueness Analysis   |
| data_type_summary    | JSONB     | Column Types          |
| generated_at         | TIMESTAMP | Profile Date          |

---

## Why JSONB?

Profiling results vary by dataset structure.

JSONB provides flexibility without creating unnecessary tables.

---

# 8. Quality Score Table

Table Name:

quality_scores

---

## Purpose

Stores dataset quality metrics.

---

### Fields

| Field              | Type         | Description |
| ------------------ | ------------ | ----------- |
| id                 | UUID         | Primary Key |
| dataset_id         | FK           | Dataset     |
| completeness_score | DECIMAL(5,2) |             |
| consistency_score  | DECIMAL(5,2) |             |
| validity_score     | DECIMAL(5,2) |             |
| uniqueness_score   | DECIMAL(5,2) |             |
| overall_score      | DECIMAL(5,2) |             |
| generated_at       | TIMESTAMP    |             |

---

## Example

```text
Completeness: 92.50
Consistency: 88.40
Validity: 95.00
Uniqueness: 100.00

Overall: 93.98
```

---

# 9. Cleaning Job Table

Table Name:

cleaning_jobs

---

## Purpose

Tracks cleaning operations.

Provides auditability and future job monitoring.

---

### Fields

| Field            | Type        | Description      |
| ---------------- | ----------- | ---------------- |
| id               | UUID        | Primary Key      |
| dataset_id       | FK          | Dataset          |
| status           | VARCHAR(50) | Job Status       |
| recommendations  | JSONB       | Suggested Fixes  |
| selected_actions | JSONB       | User Choices     |
| summary          | JSONB       | Cleaning Results |
| started_at       | TIMESTAMP   |                  |
| completed_at     | TIMESTAMP   |                  |

---

## Status Values

```text
PENDING
RUNNING
COMPLETED
FAILED
```

---

# 10. Report Table

Table Name:

reports

---

## Purpose

Stores generated report metadata.

---

### Fields

| Field        | Type         | Description |
| ------------ | ------------ | ----------- |
| id           | UUID         | Primary Key |
| dataset_id   | FK           | Dataset     |
| report_type  | VARCHAR(50)  |             |
| file_path    | VARCHAR(500) |             |
| generated_at | TIMESTAMP    |             |

---

## Report Types

```text
PDF
EXCEL
```

---

# 11. Dataset Status Lifecycle

The dataset status field tracks progress.

---

## Allowed Statuses

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

## Workflow

```text
UPLOADED
     |
     v
PROFILING
     |
     v
PROFILED
     |
     v
REVIEW_PENDING
     |
     v
CLEANING
     |
     v
COMPLETED
```

---

# 12. Relationships

## User → Dataset

Relationship:

One-to-Many

```text
User
 |
 +---- Dataset
```

A user can own multiple datasets.

---

## Dataset → DatasetVersion

Relationship:

One-to-Many

```text
Dataset
 |
 +---- DatasetVersion
```

---

## Dataset → DatasetProfile

Relationship:

One-to-One

```text
Dataset
 |
 +---- DatasetProfile
```

---

## Dataset → QualityScore

Relationship:

One-to-One

```text
Dataset
 |
 +---- QualityScore
```

---

## Dataset → CleaningJob

Relationship:

One-to-Many

```text
Dataset
 |
 +---- CleaningJob
```

---

## Dataset → Report

Relationship:

One-to-Many

```text
Dataset
 |
 +---- Report
```

---

# 13. Storage Considerations

Files themselves are not stored inside PostgreSQL.

Only metadata and file paths are stored.

---

## Example

```text
Database

dataset.original_file

/media/datasets/sales.csv
```

Actual file remains on disk.

---

# 14. Future Database Enhancements

Version 2:

* Dataset comparison
* Dataset tags
* User profiles

Version 3:

* Team workspaces
* Shared datasets

Version 4:

* Billing
* Subscription plans
* Usage analytics

---

# 15. Database Decisions Summary

| Area               | Decision              |
| ------------------ | --------------------- |
| Database Engine    | PostgreSQL            |
| Primary Keys       | UUID                  |
| User Management    | Django Auth           |
| File Storage       | Disk + Metadata in DB |
| Profiling Storage  | JSONB                 |
| Quality Metrics    | Relational Fields     |
| Cleaning Results   | JSONB                 |
| Dataset Versioning | Enabled               |
| Report Tracking    | Enabled               |
| Job Tracking       | Enabled               |

---

# 16. Database Approval

This database design serves as the foundation for all Django models, APIs, business logic, reporting modules, and future platform expansion.
