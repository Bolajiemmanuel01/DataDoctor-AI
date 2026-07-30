# DataDoctor AI

DataDoctor AI is a SaaS platform for automated dataset profiling, data quality assessment, data cleaning, and reporting.

## Tech Stack

- Django
- PostgreSQL
- Docker
- Pandas
- NumPy
- OpenPyXL
- ReportLab

## Status

Milestone 0 - Environment Setup

## Proof of Concept (POC) summary

This repository contains a lightweight POC that demonstrates the core end-to-end flow:

- Dataset upload (CSV/XLSX)
- Automated profiling (row/column counts, missing values, duplicates, types)
- Rule-based cleaning recommendations
- Cleaning engine (duplicates, missing values, text/date standardization, type fixes)
- Export cleaned artifacts (CSV/XLSX) and job audit records

The POC is Docker-first and intended to be runnable locally using the included `docker-compose.yml`.

## Quickstart (POC)

1. Copy `.env.example` to `.env` and update secrets if needed.
2. Build and start services with Docker Compose:

```powershell
docker-compose build
docker-compose up
```

3. Create database migrations and a superuser (if running Django locally):

```powershell
# inside the web container or with python environment
python manage.py migrate
python manage.py createsuperuser
```

4. Open the web UI at `http://localhost:8000/` (or the URL shown by Docker Compose).

## POC limitations and guidance

- Background processing: POC uses an in-process background worker for cleaning jobs (threaded). This is simple for demos but not suitable for production. See `docs/async_processing.md` for migration notes.
- Storage: media files are stored on local filesystem in the POC. For production, use object storage (S3 or compatible) and signed URLs.
- Security: POC provides basic Django auth. Production should add SSO/SSO, RBAC, and stricter secrets management.
- File sizes: POC does not support streaming/chunked processing. Large files may exhaust memory.

## Where to find important docs

- Architecture and POC details: `docs/03_Architecture.md`
- Async processing strategy: `docs/async_processing.md`
- AI design and explainability: `docs/ai_design.md`
- API design: `docs/05_API_Design.md`
- Development setup: `docs/07_Development_Setup.md`

## Next steps (POC → Prod)

Primary priorities to make this POC production-ready:

1. Move cleaning jobs to a task queue (Celery/RQ) and run workers.
2. Migrate media to cloud object storage (S3) and serve signed URLs.
3. Implement quotas, file-size limits, and job cost estimation.
4. Add observability (metrics, logs, traces) and monitoring dashboards.
5. Harden security (SSO, RBAC, encryption at rest) and compliance features.

See `docs/15_Development_Roadmap.md` for a detailed roadmap.