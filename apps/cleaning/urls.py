from django.urls import path

from .views import (
    CleaningJobDetailView,
    CleaningHistoryListView,
    DownloadCleanedDatasetView,
)

app_name = "cleaning"

urlpatterns = [
    path(
        "job/<uuid:job_id>/",
        CleaningJobDetailView.as_view(),
        name="job_detail",
    ),
    path(
        "history/",
        CleaningHistoryListView.as_view(),
        name="history",
    ),
    path(
        "job/<uuid:job_id>/download/<str:file_format>/",
        DownloadCleanedDatasetView.as_view(),
        name="download",
    ),
]
