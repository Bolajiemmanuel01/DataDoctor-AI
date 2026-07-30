from django.urls import path

from .views import (
    CleanDatasetAPIView,
    CleaningJobDetailAPIView,
)

app_name = "api"

urlpatterns = [
    path(
        "datasets/<uuid:dataset_id>/clean/",
        CleanDatasetAPIView.as_view(),
        name="dataset_clean",
    ),
    path(
        "datasets/<uuid:dataset_id>/profile/",
        DatasetProfileAPIView.as_view(),
        name="dataset_profile",
    ),
    path(
        "datasets/<uuid:dataset_id>/recommendations/",
        RecommendationsAPIView.as_view(),
        name="dataset_recommendations",
    ),
    path(
        "datasets/<uuid:dataset_id>/download/",
        DatasetDownloadAPIView.as_view(),
        name="dataset_download",
    ),
    path(
        "cleaning-jobs/<uuid:job_id>/",
        CleaningJobDetailAPIView.as_view(),
        name="cleaning_job_detail",
    ),
]
