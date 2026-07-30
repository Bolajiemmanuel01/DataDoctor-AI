from config.celery import app

from apps.cleaning.services.cleaning_service import CleaningService


@app.task(bind=True)
def run_cleaning_task(self, job_id, dataset_id, config):
    """Celery task wrapper that delegates to CleaningService._run_cleaning_worker.

    The heavy lifting remains in the service layer; the task simply invokes it
    so the worker process executes the same logic as the POC thread worker.
    """

    # Delegate to the service's internal worker function if available
    CleaningService._run_cleaning_worker(job_id, dataset_id, config)
