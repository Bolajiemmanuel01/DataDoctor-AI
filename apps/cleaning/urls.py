from django.urls import path

from .views import (
    RunCleaningView,
    CleaningJobDetailView,
)

app_name = "cleaning"

urlpatterns = [

    path(
        "run/<uuid:dataset_id>/",
        RunCleaningView.as_view(),
        name="run",
    ),

    path(
        "job/<uuid:job_id>/",
        CleaningJobDetailView.as_view(),
        name="detail",
    ),
]