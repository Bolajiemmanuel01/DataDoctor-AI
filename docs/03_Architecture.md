# Solution Architecture Document

## Project Name

**DataDoctor AI**

---

# 1. Architecture Overview

DataDoctor AI is designed as a modular SaaS platform that enables users to upload datasets, analyze data quality, apply cleaning operations, generate reports, and download cleaned datasets.

The architecture prioritizes:

* Simplicity for MVP delivery
* Maintainability
* Scalability
* Security
* Future cloud readiness

The platform will initially operate as a monolithic Django application deployed using Docker containers while maintaining clear module boundaries to support future service extraction if required.

---

# 2. Architectural Principles

The following principles guide all technical decisions:

## Modular Design

Each business capability is isolated into its own Django application.

Benefits:

* Easier maintenance
* Better testability
* Cleaner code organization

---

## Separation of Concerns

Business logic, presentation logic, and data access logic must remain separate.

Benefits:

* Reduced complexity
* Easier debugging
* Better scalability

---

## SaaS Readiness

Although the MVP serves individual users, the architecture must support future:

* Subscription plans
* Team workspaces
* API access
* Multi-tenancy

without requiring major redesign.

---

## Docker First

All services run inside containers.

Benefits:

* Consistent development environments
* Easier deployment
* Simplified onboarding

---

# 3. High-Level System Architecture

```text
+--------------------+
|     Web Browser    |
+---------+----------+
          |
          v
+--------------------+
| Django Web App     |
+---------+----------+
          |
          |
          +------------------+
          |                  |
          v                  v
+----------------+    +----------------+
| PostgreSQL DB  |    | File Storage   |
+----------------+    +----------------+
          |
          v
+--------------------+
| Reports & Exports  |
+--------------------+
```

---

# 4. User Workflow Architecture

```text
User Registration
        |
        v
User Login
        |
        v
Upload Dataset
        |
        v
Dataset Stored
        |
        v
Profiling Engine
        |
        v
Quality Assessment
        |
        v
Issue Review Screen
        |
        v
User Approves Cleaning
        |
        v
Cleaning Engine
        |
        v
Generate Reports
        |
        v
Download Cleaned Dataset
```

---

# 5. Technology Stack

## Frontend

* Django Templates
* Bootstrap 5
* HTML5
* CSS3
* JavaScript

### Why

Allows rapid MVP development while remaining compatible with future frontend frameworks.

---

## Backend

* Python
* Django

### Why

Provides:

* Fast development
* Strong security
* Excellent ecosystem
* Strong data processing support

---

## Database

PostgreSQL

### Why

* Production-ready
* Reliable
* Scalable
* Strong relational capabilities

---

## Data Processing

### Libraries

* Pandas
* NumPy

### Why

Industry-standard tools for:

* Profiling
* Data transformation
* Cleaning
* Statistical analysis

---

## Reporting

### Excel Reports

OpenPyXL

### PDF Reports

ReportLab

### Why

Allows professional report generation directly from Python.

---

## Containerization

* Docker
* Docker Compose

### Why

Provides reproducible environments and deployment consistency.

---

# 6. Docker Architecture

The MVP uses two containers.

```text
+---------------------+
| datadoctor-web      |
| Django Application  |
+----------+----------+
           |
           v
+---------------------+
| datadoctor-db       |
| PostgreSQL          |
+---------------------+
```

Future containers may include:

```text
datadoctor-worker
datadoctor-redis
datadoctor-nginx
```

---

# 7. Django Application Architecture

Project Structure:

```text
datadoctor-ai/

apps/
│
├── accounts/
├── datasets/
├── profiling/
├── cleaning/
├── quality/
├── reporting/
├── core/
│
docs/
docker/
config/
```

---

## accounts

Responsible for:

* Registration
* Login
* Logout
* User management

---

## datasets

Responsible for:

* Dataset upload
* Dataset storage
* Dataset history

---

## profiling

Responsible for:

* Row counts
* Column counts
* Missing value analysis
* Duplicate analysis
* Unique value analysis

---

## cleaning

Responsible for:

* Cleaning recommendations
* Cleaning execution
* Dataset export

---

## quality

Responsible for:

* Completeness score
* Consistency score
* Validity score
* Uniqueness score

---

## reporting

Responsible for:

* Excel report generation
* PDF report generation

---

## core

Responsible for:

* Shared utilities
* Constants
* Helpers
* Common services

---

# 8. Dataset Processing Architecture

The processing lifecycle is designed to maintain both original and cleaned dataset versions.

```text
Upload Dataset
        |
        v
Store Original File
        |
        v
Profile Dataset
        |
        v
Generate Quality Metrics
        |
        v
Generate Recommendations
        |
        v
User Reviews Recommendations
        |
        v
Execute Cleaning
        |
        v
Store Cleaned Dataset
        |
        v
Generate Reports
```

---

# 9. File Storage Architecture

Files are stored using Docker volumes.

Directory Structure:

```text
media/
```

---

# 10. POC vs Production Architecture

This section describes the differences between the lightweight POC deployment and a recommended production architecture.

## POC deployment

- Single Django web process (container) handling web requests and background tasks (thread-based worker).
- Local PostgreSQL (container) for metadata and job records.
- Local filesystem (`media/`) for uploaded and cleaned artifacts.

Pros: easy to run locally via Docker Compose, low setup friction.
Cons: limited scalability and resilience, unsuitable for multi-tenant production workloads.

## Production architecture (recommended)

```
Client
        |
        v
Load Balancer / CDN
        |
        v
Web/API (Django w/ Gunicorn)
        |
        +--> Message Broker (Redis/RabbitMQ)
        |        |
        |        v
        |     Worker Pool (Celery/RQ)  <---> Object Storage (S3)
        |        |
        |        v
        +--> PostgreSQL (metadata)
        |
        +--> Cache (Redis)
        |
        +--> Monitoring / Logging / Tracing
```

Key production components:

- Message broker & workers: move cleaning execution to external worker processes (Celery or RQ) to process jobs asynchronously and at scale.
- Object storage: use S3-compatible storage for originals, cleaned artifacts, and reports. Serve downloads via signed URLs.
- Cache: Redis for caching profiles, recommendation results, and reducing load on DB for frequent reads.
- Monitoring & observability: Prometheus metrics, Grafana dashboards, structured logging (ELK/Cloud provider), and OpenTelemetry tracing.
- Security & identity: SSO/SAML/OAuth2 for enterprise identity, RBAC for resource access.

## Migration notes

- Introduce a feature flag (`USE_TASK_QUEUE`) to toggle between the POC thread worker and a queue-backed worker during migration.
- Implement a storage abstraction so `DEFAULT_FILE_STORAGE` can be switched from local to S3 without changing application code.
- Add health checks for workers, queue depth monitoring, and alerts for failed jobs.

## Operational considerations

- Scale workers by queue length and job complexity (CPU/memory requirements).
- Enforce per-tenant quotas for upload sizes and concurrent jobs.
- Implement cost estimates for processing and show estimates to users for large jobs.

## References

- Async processing details: `docs/async_processing.md`
- Storage & artifact management: `docs/storage.md`
- Security considerations: `docs/security_compliance.md`
- AI recommendations design: `docs/ai_design.md`


├── datasets/
│
├── cleaned/
│
├── reports/
│
└── temp/
```

---

## datasets

Stores original uploaded files.

Examples:

```text
sales.csv
survey.xlsx
```

---

## cleaned

Stores cleaned dataset versions.

Examples:

```text
sales_cleaned.csv
survey_cleaned.xlsx
```

---

## reports

Stores generated reports.

Examples:

```text
quality_report.pdf
quality_report.xlsx
```

---

## temp

Temporary processing files.

Automatically cleared after processing.

---

# 10. Dataset Versioning Strategy

Original files must never be modified.

Workflow:

```text
Original Dataset
        |
        v
Cleaning Process
        |
        v
Cleaned Dataset
```

Benefits:

* Auditability
* Traceability
* User confidence
* Future comparison features

---

# 11. Processing Job Status Tracking

Every dataset processing operation will have a status.

Supported statuses:

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

## Example Workflow

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

# 12. Security Architecture

## Authentication

Django Authentication System

Features:

* Secure password hashing
* Session management
* Authentication middleware

---

## File Validation

Accepted formats:

* CSV
* XLSX

Rejected formats:

* EXE
* ZIP
* Unknown file types

---

## File Size Restriction

Maximum upload size:

```text
100 MB
```

---

## CSRF Protection

Django CSRF middleware enabled.

Protects forms and authenticated requests.

---

## Access Control

Users can only access:

* Their own datasets
* Their own reports
* Their own cleaned files

---

# 13. Scalability Strategy

The MVP is intentionally simple but designed for future growth.

Future Architecture:

```text
+------------------+
| Load Balancer    |
+--------+---------+
         |
         v
+------------------+
| Django App       |
+--------+---------+
         |
         +-------------------+
         |                   |
         v                   v
+----------------+   +----------------+
| PostgreSQL     |   | Redis          |
+----------------+   +----------------+
         |
         v
+----------------+
| Celery Workers |
+----------------+
         |
         v
+----------------+
| Cloud Storage  |
+----------------+
```

This allows:

* Background processing
* Large dataset handling
* Horizontal scaling
* Cloud deployments

without redesigning the application.

---

# 14. Architecture Decisions Summary

| Decision          | Selected Option              |
| ----------------- | ---------------------------- |
| Authentication    | Included from Day One        |
| Dataset Ownership | Enabled                      |
| Dataset History   | Enabled                      |
| Upload Limit      | 100 MB                       |
| Storage Strategy  | Docker Volumes               |
| Database          | PostgreSQL                   |
| Backend           | Django                       |
| Data Processing   | Pandas + NumPy               |
| Reporting         | OpenPyXL + ReportLab         |
| Containerization  | Docker + Docker Compose      |
| Cleaning Workflow | User Reviews Before Cleaning |
| Versioning        | Original + Cleaned Files     |
| Job Tracking      | Enabled                      |

---

# 15. Architecture Approval

This document defines the approved architecture for the DataDoctor AI MVP and serves as the technical blueprint for database design, API design, development, testing, and deployment.
