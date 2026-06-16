from django.db import models

from django.conf import settings

from apps.core.models import BaseModel

from .validators import validate_dataset_file

class DatasetStatus(models.TextChoices):
    UPLOADED = "UPLOADED", "Uploaded"
    PROFILING = "PROFILING", "Profiling"
    PROFILED = "PROFILED", "Profiled"
    REVIEW_PENDING = "REVIEW_PENDING", "Review Pending"
    CLEANING = "CLEANING", "Cleaning"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class Dataset(BaseModel):
    """
    Represents a dataset uploaded by a user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="datasets"
    )

    name = models.CharField(
        max_length=255
    )

    original_file = models.FileField(
        upload_to="datasets/",
        validators=[validate_dataset_file],
    )

    file_type = models.CharField(
        max_length=20
    )

    file_size = models.BigIntegerField()
    
    status = models.CharField(
        max_length=50,
        choices=DatasetStatus.choices,
        default=DatasetStatus.UPLOADED
    )

    class Meta:
        ordering = ["-created_at"]
    
    def save(self, *args, **kwargs):

        if self.original_file:

            self.file_size = self.original_file.size

            filename = self.original_file.name.lower()

            if filename.endswith(".csv"):
                self.file_type = "csv"

            elif filename.endswith(".xlsx"):
                self.file_type = "xlsx"

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    
