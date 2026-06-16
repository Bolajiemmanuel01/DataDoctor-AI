from django.contrib import admin

from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "file_type",
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "user__username",
    )

    list_filter = (
        "status",
        "file_type",
    )