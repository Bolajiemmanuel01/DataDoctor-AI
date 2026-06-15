# Milestone 0 – Development Environment & Project Setup

## Project Name

**DataDoctor AI**

---

# 1. Milestone Overview

This milestone establishes the development foundation for DataDoctor AI.

No business functionality will be developed during this milestone.

The objective is to create a stable, reproducible, Docker-based environment that will support future development.

---

# 2. Milestone Objective

By the end of this milestone, we should have:

* Git repository initialized
* Project folder structure created
* Docker configured
* PostgreSQL running in Docker
* Django project running in Docker
* Environment variables configured
* Database connection verified

---

# 3. Why This Milestone Exists

Many projects fail because development begins before infrastructure is stable.

This milestone ensures:

* Consistent environments
* Reliable onboarding
* Simplified deployment
* Reduced configuration issues

---

# 4. Repository Structure

The repository should be organized as follows:

```text
datadoctor-ai/

├── apps/
│
├── config/
│
├── docs/
│
├── docker/
│
├── media/
│
├── static/
│
├── tests/
│
├── requirements/
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── README.md
```

---

# 5. Folder Responsibilities

## apps/

Contains all Django applications.

Examples:

```text
accounts/
datasets/
profiling/
cleaning/
quality/
reporting/
core/
```

---

## config/

Contains project configuration.

Examples:

```text
settings.py
urls.py
wsgi.py
asgi.py
```

---

## docs/

Project documentation.

---

## docker/

Docker-related files.

Examples:

```text
entrypoint.sh
postgres/
```

---

## media/

User-generated files.

Examples:

```text
datasets/
cleaned/
reports/
temp/
```

---

## tests/

Automated tests.

---

## requirements/

Dependency management.

Examples:

```text
base.txt
development.txt
production.txt
```

---

# 6. Git Repository Setup

Repository Name:

```text
datadoctor-ai
```

Recommended Initial Branches:

```text
main
develop
```

---

# 7. Docker Architecture

Two containers will be created.

---

## Django Container

Container Name:

```text
datadoctor-web
```

Responsibilities:

* Django application
* API endpoints
* Business logic
* Report generation

---

## PostgreSQL Container

Container Name:

```text
datadoctor-db
```

Responsibilities:

* Data persistence
* Application database

---

# 8. Environment Variables

All configuration must use environment variables.

---

## Required Variables

```env
DEBUG=True

SECRET_KEY=change-me

ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=datadoctor

DB_USER=datadoctor

DB_PASSWORD=datadoctor

DB_HOST=db

DB_PORT=5432
```

---

# 9. Required Python Packages

Core:

```text
Django
psycopg2-binary
python-dotenv
```

---

Data Processing:

```text
pandas
numpy
openpyxl
```

---

Reporting:

```text
reportlab
```

---

Testing:

```text
pytest
pytest-django
coverage
```

---

# 10. Media Storage Structure

Create:

```text
media/

├── datasets/
├── cleaned/
├── reports/
└── temp/
```

Purpose:

### datasets/

Stores original uploads.

---

### cleaned/

Stores cleaned datasets.

---

### reports/

Stores generated reports.

---

### temp/

Temporary processing files.

---

# 11. Docker Volume Strategy

Persist data outside containers.

Required Volumes:

```text
postgres_data

media_data
```

Benefits:

* Database survives container recreation
* Uploaded files remain available

---

# 12. Initial Validation Tests

The following must pass before Milestone 0 is complete.

---

## Docker Validation

Checklist:

* Docker starts successfully
* Containers build successfully
* Containers communicate

---

## PostgreSQL Validation

Checklist:

* PostgreSQL container starts
* Database created
* Django connects successfully

---

## Django Validation

Checklist:

* Django starts successfully
* Admin page accessible
* Migrations run successfully

---

## Volume Validation

Checklist:

* Files persist after restart
* Database persists after restart

---

# 13. Deliverables

At completion of Milestone 0:

* Dockerfile
* docker-compose.yml
* Django project initialized
* PostgreSQL configured
* Environment variables configured
* Git repository initialized

---

# 14. Documentation Updates

Upon completion update:

* Architecture Document
* Deployment Strategy
* README

if any changes occur.

---

# 15. Recommended Git Commits

Repository Initialization:

```bash
git commit -m "chore: initialize repository structure"
```

Docker Setup:

```bash
git commit -m "feat: add docker development environment"
```

Database Configuration:

```bash
git commit -m "feat: configure postgresql integration"
```

Django Initialization:

```bash
git commit -m "feat: initialize django project"
```

---

# 16. Milestone Approval Criteria

Milestone 0 is considered complete when:

* Docker environment operational
* PostgreSQL operational
* Django operational
* Database connectivity verified
* Volume persistence verified
* Documentation updated

No business functionality should be implemented during this milestone.

---

# 17. Next Milestone

Milestone 1:

Dataset Upload & Profiling Engine

Deliverables:

* Authentication module
* Dataset upload
* Dataset storage
* Dataset profiling
* Profiling dashboard

This is the first feature milestone of DataDoctor AI.
