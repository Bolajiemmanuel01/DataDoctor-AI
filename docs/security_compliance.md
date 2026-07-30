# Security, Privacy & Compliance (POC → Prod)

This document outlines security and compliance considerations for the POC and recommended production hardening steps.

## POC posture

- Authentication: basic Django authentication with username/password.
- Authorization: dataset ownership enforced at the view level (queryset filtering). No multi-tenant isolation or RBAC in POC.
- Secrets: environment variables in `.env` (local). No secret management service configured.

## Production requirements

1. Authentication & Identity

   - Add SSO/SAML/OAuth2 support for enterprise customers.
   - Support SCIM for user provisioning.

2. Authorization & Multi‑Tenancy

   - Implement RBAC and tenant-aware scoping (tenant_id on resources) or schema-per-tenant as appropriate.
   - Enforce per-tenant quotas and resource limits.

3. Data Protection

   - Encrypt data at rest (object storage + DB encryption where supported).
   - Enforce TLS for all transport.
   - Use signed URLs for temporary downloads.

4. Secrets & Configuration

   - Do not store secrets in plaintext or in source control.
   - Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) or managed parameter store.

5. Auditability & Logging

   - Record audit logs for dataset uploads, cleaning job triggers, downloads, and configuration changes.
   - Persist logs in a centralized system with tamper-resistant retention policies.

6. Privacy & Data Minimization

   - Provide data deletion workflows and customer-controlled retention policies.
   - Anonymize or pseudonymize data used for model training.

7. Compliance

   - Prepare for GDPR, HIPAA (if handling PHI), and other regional regulations as required by customers.
   - Offer data residency options for enterprise customers.

8. Operational Security

   - Harden container images, scan for vulnerabilities, and keep dependencies updated.
   - Implement network segmentation and least-privilege IAM policies for service accounts.

## POC→Prod checklist

- Integrate SSO and RBAC.
- Move secrets to a secrets manager and remove `.env` from source-controlled environments.
- Add encryption-at-rest for storage and database-level protections.
- Add audit logging and retention policies.
- Add secure defaults for file upload validation (MIME/type checks, size limits, row count limits).

## Recommended acceptance criteria for production readiness

- All sensitive data encrypted at rest and in transit.
- Role-based access control and tenant isolation enforced.
- Audit trail for all data transformations and downloads.
- Regular security scans and vulnerability management process.
