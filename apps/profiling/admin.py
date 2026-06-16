from django.contrib import admin

from .models import DatasetProfile


@admin.register(DatasetProfile)
class DatasetProfileAdmin(admin.ModelAdmin):
    list_display = (
        "dataset",
        "row_count",
        "column_count",
        "duplicate_rows",
        "generated_at"
    )