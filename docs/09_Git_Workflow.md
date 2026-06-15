# Git Workflow

## Project Name

**DataDoctor AI**

---

# 1. Purpose

This document defines the Git workflow for DataDoctor AI.

The goal is to ensure:

* Clean version history
* Easy collaboration
* Controlled releases
* Traceable changes

---

# 2. Repository Structure

Primary Repository:

```text
datadoctor-ai
```

Hosted on GitHub.

---

# 3. Branching Strategy

The project follows a simplified Git Flow model.

---

## Main Branch

```text
main
```

Purpose:

Production-ready code only.

Rules:

* Direct commits prohibited
* Pull requests required

---

## Development Branch

```text
develop
```

Purpose:

Integration branch for completed features.

---

## Feature Branches

Naming Convention:

```text
feature/<feature-name>
```

Examples:

```text
feature/authentication

feature/dataset-upload

feature/profiling-engine

feature/reporting-module
```

---

## Bug Fix Branches

Naming Convention:

```text
bugfix/<bug-name>
```

Examples:

```text
bugfix/login-validation

bugfix/profile-generation
```

---

# 4. Commit Message Standards

Format:

```text
<type>: <description>
```

---

## Types

### Feature

```text
feat: add dataset upload functionality
```

---

### Fix

```text
fix: resolve duplicate detection issue
```

---

### Documentation

```text
docs: update architecture document
```

---

### Refactor

```text
refactor: simplify profiling service
```

---

### Test

```text
test: add quality score tests
```

---

### Chore

```text
chore: update dependencies
```

---

# 5. Pull Request Process

Every pull request should include:

* Description
* Related issue
* Testing completed
* Documentation updates

---

## Checklist

Before approval:

* Code reviewed
* Tests passing
* Documentation updated
* No merge conflicts

---

# 6. Release Process

Release workflow:

```text
Feature Branch
       ↓
Develop Branch
       ↓
Main Branch
       ↓
Release Tag
```

---

# 7. Versioning Strategy

Semantic Versioning:

Format:

```text
MAJOR.MINOR.PATCH
```

Examples:

```text
1.0.0

1.1.0

1.1.1
```

---

## Meaning

### Major

Breaking changes.

---

### Minor

New features.

---

### Patch

Bug fixes.

---

# 8. Git Ignore Policy

Exclude:

```text
.env

__pycache__/

*.pyc

media/

staticfiles/

.vscode/

.idea/
```

---

# 9. Git Workflow Approval

This workflow governs source control for DataDoctor AI.
