# Async Processing Strategy (POC → Prod)

This document describes the background processing approach used in the POC and the recommended migration path to a production-ready task queue architecture.

## POC behaviour

- The POC enqueues `CleaningJob` records and processes cleaning tasks using a background thread started by the web process. This keeps the demo simple and requires no external infrastructure.
- Advantages: zero infra dependencies, easy to run in Docker Compose, quick feedback loop for development.
- Limitations: not resilient, not horizontally scalable, can block the web process or be OOMed by large jobs, lacks retries and observability.

## Production requirements

Production systems should satisfy the following:

- Reliable asynchronous execution with retries and backoff.
- Horizontal scaling of workers.
- Visibility: job metrics, logs, and tracing.
- Safe isolation of heavy workloads to prevent web layer disruption.

## Recommended architecture

Adopt a worker-based task queue such as Celery (Redis/RabbitMQ broker) or RQ (Redis). Components:

- Web service (Django) — enqueues tasks and serves API/UI.
- Message broker (Redis/RabbitMQ) — durable task queue.
- Worker processes — execute cleaning jobs in isolated processes/containers.
- Result backend / database — job metadata stored in `CleaningJob` model; workers update status and artifacts.
- Object storage (S3) — store original and cleaned artifacts.

Example flow:

1. User submits cleaning request (UI or API).
2. Web service creates `CleaningJob` row with status `PENDING` and enqueues a task.
3. Worker picks up the task, updates `CleaningJob` to `RUNNING`, processes, saves artifacts to storage, updates `CleaningJob` to `COMPLETED` or `FAILED`.
4. Web/UI polls job status or receives a webhook when job completes.

## Migration checklist (POC → Celery)

1. Add Celery to the project and configure broker (Redis/RabbitMQ) and result backend.
2. Replace in-process worker threading code with a Celery task that accepts `job_id` and `config`.
3. Ensure workers run in separate containers with resource limits (CPU, memory).
4. Persist intermediate status updates to `CleaningJob` and log progress.
5. Implement idempotency checks and safe retries (avoid re-processing completed jobs).
6. Add monitoring for queue length, worker health, and job latency.

## Operational considerations

- Resource quotas per tenant to avoid noisy neighbors.
- Timeouts for long-running tasks and a mechanism to cancel jobs.
- Back-pressure and rate limiting for job submissions.
- Graceful worker shutdown and task requeuing on failure.

## Short-term POC improvements (low-effort)

- Add a `USE_TASK_QUEUE` feature flag in settings (default: `false`) to allow toggling between thread worker and queue-backed workers.
- Add structured logging around job lifecycle events.
- Add a simple webhook or SSE for job completion events for the UI to subscribe to.

## Long-term

- Add autoscaling for workers based on queue length and job duration.
- Integrate with managed task services (AWS SQS + Lambda, Google Cloud Tasks) for serverless scaling where appropriate.
