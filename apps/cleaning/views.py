from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, RedirectView

from apps.datasets.models import Dataset
from .models import CleaningJob
from .services.cleaning_service import CleaningService

class RunCleaningView(
    LoginRequiredMixin,
    RedirectView
):

    def get_redirect_url(
        self,
        *args,
        **kwargs
    ):

        dataset = get_object_or_404(
            Dataset,
            id=kwargs["dataset_id"],
            user=self.request.user
        )

        job = (
            CleaningService.remove_duplicates(
                dataset
            )
        )

        return reverse(
            "cleaning:detail",
            kwargs={
                "job_id": job.id
            }
        )

class CleaningJobDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = CleaningJob

    template_name = (
        "cleaning/detail.html"
    )

    context_object_name = "job"

    pk_url_kwarg = "job_id"