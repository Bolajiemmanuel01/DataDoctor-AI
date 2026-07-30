# Storage & Artifact Management (POC → Prod)

This document describes how files and artifacts are stored in the POC, recommendations for production, and migration steps.

## POC behavior

- By default the POC stores uploaded datasets and cleaned artifacts on the local filesystem under `media/`.
- Files are written by Django `FileField` attributes and served by `django.views.static.serve` in DEBUG mode or by the web server when configured.

## Production recommendations

- Use S3-compatible object storage for all user-uploaded artifacts (originals, cleaned outputs, reports, temp exports).
- Keep originals immutable; never overwrite the original file. Store cleaned outputs as separate objects with versioned keys.
- Use signed (time-limited) URLs for downloads rather than serving files through the web server.
- Apply lifecycle policies (e.g., move to colder storage after X days) and retention rules per customer plan.

## Naming conventions

- Original: `datasets/{dataset_id}/original/{filename}`
- Cleaned CSV: `datasets/{dataset_id}/cleaned/{job_id}/{dataset_id}_cleaned.csv`
- Cleaned XLSX: `datasets/{dataset_id}/cleaned/{job_id}/{dataset_id}_cleaned.xlsx`
- Reports: `datasets/{dataset_id}/reports/{report_id}.pdf`

## Access control

- Store metadata and object keys in the database (e.g., `CleaningJob.cleaned_csv_file.name`). Use database records to authorize access.
- Serve downloads via signed URLs that the application generates after verifying permissions.

## Migration steps (local → S3)

1. Implement a storage backend abstraction (Django `DEFAULT_FILE_STORAGE`) and configuration options for local vs S3.
2. Add migration scripts to copy existing `media/` objects to S3 and update database file paths to point to new keys.
3. Update download endpoints to return signed URLs for S3 objects.
4. Add retention policies and lifecycle rules for buckets.

## Cost & operational notes

- Track storage usage per tenant and expose quotas. Consider per-GB billing or tier-based quotas.
- Clean temporary/export directories promptly; use background workers to delete intermediate files after upload to storage.

## Local development guidance

- Keep `MEDIA_ROOT` pointing to `media/` for quick iteration. Set `DEBUG=True` only in dev.
- Use a local S3 emulator (e.g., MinIO) to test S3-backed behavior without external cloud access.
