# Development Setup Guide

## Project Name

**DataDoctor AI**

---

# 1. Overview

This document defines the local development environment required to build and run DataDoctor AI.

The goal is to ensure every developer can run the project using a consistent setup regardless of machine configuration.

---

# 2. Development Principles

The project follows a Docker-first approach.

Requirements:

* No local PostgreSQL installation
* No local Python virtual environments required
* All services run through Docker containers
* Configuration managed through environment variables

---

# 3. Development Environment

## Operating System

Supported:

* Windows 11 (Primary)
* Windows 10
* Linux
* macOS

---

# 4. Required Software

## Git

Purpose:

Version control.

Recommended Version:

Latest Stable Release.

---

## Docker Desktop

Purpose:

Container runtime.

Required Features:

* Docker Engine
* Docker Compose

---

## Visual Studio Code

Recommended IDE.

Suggested Extensions:

* Python
* Docker
* GitLens
* PostgreSQL
* YAML

---

# 5. Project Structure

```text
datadoctor-ai/

├── apps/
├── config/
├── docs/
├── docker/
├── media/
├── static/
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── README.md
```

---

# 6. Environment Variables

All configuration must be stored in environment variables.

Example:

```env
DEBUG=True

SECRET_KEY=replace-me

ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=datadoctor

DB_USER=datadoctor

DB_PASSWORD=datadoctor

DB_HOST=db

DB_PORT=5432
```

---

# 7. Docker Services

## Web Service

Container Name:

```text
datadoctor-web
```

Purpose:

Runs Django application.

---

## Database Service

Container Name:

```text
datadoctor-db
```

Purpose:

Runs PostgreSQL.

---

# 8. Media Storage

Development storage:

```text
media/

├── datasets/
├── cleaned/
├── reports/
└── temp/
```

All folders mounted as Docker volumes.

---

# 9. Local Development Workflow

```text
Clone Repository
        ↓
Create .env File
        ↓
Build Docker Containers
        ↓
Run Migrations
        ↓
Create Superuser
        ↓
Start Development
```

---

# 10. Database Management

Database runs entirely inside Docker.

No local PostgreSQL installation required.

Database persistence provided through Docker volumes.

---

# 11. Logging

Development logging:

* Console logging
* Error logging
* Django debug logging

Future:

* Structured logging
* Centralized monitoring

---

# 12. Development Approval

This document defines the standard development environment for all contributors.
