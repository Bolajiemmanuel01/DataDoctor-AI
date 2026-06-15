# Coding Standards

## Project Name

**DataDoctor AI**

---

# 1. Purpose

This document defines coding standards and best practices for DataDoctor AI.

The objective is to ensure:

* Readability
* Consistency
* Maintainability
* Scalability

---

# 2. Python Standards

Follow:

* PEP 8
* Django Best Practices

---

# 3. Naming Conventions

## Variables

```python
dataset_name
row_count
quality_score
```

---

## Functions

```python
calculate_quality_score()

generate_profile()

clean_dataset()
```

---

## Classes

```python
DatasetProfileService

QualityScoreCalculator

ReportGenerator
```

---

# 4. Django Standards

Business logic must not live inside views.

Use:

* Services
* Utilities
* Managers

Views should remain lightweight.

---

# 5. Database Standards

Use UUID primary keys.

Example:

```python
id = models.UUIDField(...)
```

Avoid integer IDs for business entities.

---

# 6. Comments

Explain:

* Why code exists
* Business logic
* Complex calculations

Avoid commenting obvious code.

---

# 7. Testing Requirements

Every new feature should include:

* Unit tests
* Integration tests (where applicable)

---

# 8. Code Review Requirements

Code should be reviewed for:

* Readability
* Security
* Performance
* Test coverage

---

# 9. Documentation Requirements

Every milestone must update:

* Architecture documentation
* API documentation
* Testing documentation

---

# 10. Coding Standards Approval

These standards apply to all DataDoctor AI development.
