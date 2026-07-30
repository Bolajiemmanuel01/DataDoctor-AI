# Testing, Observability & Performance Guidance

This document describes recommended tests, monitoring, and performance checks for the POC and migration to production.

## Testing strategy

- Unit tests: cover core services (profiling, recommendation, cleaning rules) with small datasets.
- Integration tests: end-to-end flows for upload → profile → recommend → clean → download (already present under `apps/*/tests.py`).
- Edge-case tests: invalid formats, corrupted files, malicious CSVs (e.g., formula injection), permission checks, invalid configs.
- Large-file and stress tests: simulate large CSV/XLSX files to validate memory usage and worker behavior; use chunking or streaming where required.
- Regression tests: persist a suite of sample datasets and expected profile/clean outputs to detect regressions in cleaning logic.

## Observability

- Metrics to expose (Prometheus):
  - `jobs_submitted_total`
  - `jobs_completed_total`
  - `jobs_failed_total`
  - `job_duration_seconds` (histogram)
  - `jobs_in_queue`
- Logs:
  - Structured JSON logs containing `job_id`, `dataset_id`, `user_id`, `event`, and `message`.
  - Separate error logs and access logs.
- Tracing:
  - Add distributed tracing for multi-component flows (web → queue → worker) using OpenTelemetry.

## Performance guidance

- Memory: avoid full in-memory processing for very large files; prefer chunked processing or Dask for out-of-core.
- Timeouts: set sensible timeouts for jobs and HTTP requests; provide cancellation endpoints.
- Concurrency: run workers in separate containers with CPU/memory limits to protect web nodes.

## Alerts & SLOs

- Alert on worker failures, high error rates, and queue backlog growth.
- Define SLOs for job success rate (e.g., 99%) and job latency (e.g., 95% of jobs < 60s for small datasets).

## Test harness & CI recommendations

- Add a dedicated test runner job in CI that runs unit and integration tests on each PR.
- For heavy tests (large-file), run as a periodic pipeline or gated integration job.
