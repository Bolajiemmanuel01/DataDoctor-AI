# API OpenAPI Stub (POC)

This file documents a minimal OpenAPI-style reference for the POC endpoints. It is intentionally small and written to help clients interact with the POC API.

## Base

Base path: `/api/v1/`

## Endpoints

1. POST `/api/v1/datasets/{dataset_id}/clean/`

   - Description: Trigger a cleaning job for a dataset. Accepts an optional JSON cleaning config. If omitted, defaults are used.
   - Auth: Session cookie (login required)
   - Request body (JSON, optional): cleaning configuration. Example:

```json
{
  "remove_duplicates": true,
  "handle_missing_values": false,
  "standardize_text": {"enabled": true, "columns": ["name"]},
  "standardize_dates": {"enabled": true, "columns": ["date"], "parsing_mode": "auto"}
}
```

   - Success response (200):

```json
{ "success": true, "job_id": "<uuid>", "status": "PENDING" }
```

2. GET `/api/v1/cleaning-jobs/{job_id}/`

   - Description: Fetch cleaning job metadata and summary.
   - Success response (200):

```json
{ "success": true, "job": { "id": "<uuid>", "status": "COMPLETED", "cleaning_summary": { /* ... */ } } }
```

3. GET `/api/v1/datasets/{dataset_id}/profile/`

   - Description: Get the computed profile for a dataset.

4. GET `/api/v1/datasets/{dataset_id}/recommendations/`

   - Description: Get cleaning recommendations for a dataset.

5. GET `/api/v1/datasets/{dataset_id}/download/`

   - Description: Get URLs for the most recent cleaned artifacts (CSV/XLSX). The POC returns internal download paths; production should return signed object-storage URLs.

## Notes and next steps

- This stub is a convenience reference. For production, generate a full OpenAPI/Swagger spec and publish client SDKs.
- Add response codes, error schemas, and authentication schemes in the full OpenAPI spec.
