from django.db import models

from apps.core.models import BaseModel
from apps.datasets.models import Dataset


class CleaningStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"

    RUNNING = "RUNNING", "Running"

    COMPLETED = "COMPLETED", "Completed"

    FAILED = "FAILED", "Failed"


class CleaningJob(BaseModel):

    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="cleaning_jobs"
    )

    status = models.CharField(
        max_length=20,
        choices=CleaningStatus.choices,
        default=CleaningStatus.PENDING
    )

    rows_before = models.IntegerField(
        default=0
    )

    rows_after = models.IntegerField(
        default=0
    )

    duplicates_removed = models.IntegerField(
        default=0
    )

    cleaned_file = models.FileField(
        upload_to="cleaned/",
        blank=True,
        null=True
    )

    cleaning_summary = models.JSONField(
        default=dict
    )

    def __str__(self):

        return (
            f"Cleaning Job - "
            f"{self.dataset.name}"
        )