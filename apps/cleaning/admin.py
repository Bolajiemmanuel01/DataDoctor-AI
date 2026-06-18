from django.contrib import admin

from .models import CleaningJob


@admin.register(CleaningJob)
class CleaningJobAdmin(admin.ModelAdmin):

    list_display = (
        "dataset",
        "status",
        "rows_before",
        "rows_after",
        "created_at",
    )