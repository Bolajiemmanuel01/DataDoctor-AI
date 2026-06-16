from django.urls import path

from .views import (
    DatasetUploadView,
    DatasetListView,
    DatasetProfileView,
)

app_name = "datasets"

urlpatterns = [
    path(
        "upload/",
        DatasetUploadView.as_view(),
        name="upload",
    ),
    path(
        "",
        DatasetListView.as_view(),
        name="list",
    ),
    path(
        "<uuid:dataset_id>/profile/",
        DatasetProfileView.as_view(),
        name="profile",
    ),
]