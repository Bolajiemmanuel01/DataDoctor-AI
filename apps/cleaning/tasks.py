from config.celery import app

from apps.cleaning.services.cleaning_service import CleaningService


@app.task(bind=True)
def run_cleaning_task(self, job_id, dataset_id, config):
    """Celery task wrapper that delegates to CleaningService._run_cleaning_worker.

    The heavy lifting remains in the service layer; the task simply invokes it
    so the worker process executes the same logic as the POC thread worker.
    """

    # Delegate to the centralized executor so worker processes run the same
    # implementation as the in-process thread used by the POC.
    CleaningService._execute_cleaning(job_id, dataset_id, config)
