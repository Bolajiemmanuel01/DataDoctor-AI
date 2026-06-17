from django.db import models

from apps.core.models import BaseModel
from apps.datasets.models import Dataset


class DatasetProfile(BaseModel):
    """
    Stores profiling results for a dataset.
    """

    dataset = models.OneToOneField(
        Dataset,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    row_count = models.IntegerField(
        default=0
    )

    column_count = models.IntegerField(
        default=0
    )

    column_names = models.JSONField(
        default=list
    )

    missing_values = models.JSONField(
        default=dict
    )

    duplicate_rows = models.IntegerField(
        default=0
    )

    unique_value_summary = models.JSONField(
        default=dict
    )

    data_type_summary = models.JSONField(
        default=dict
    )

    generated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Profile - {self.dataset.name}"