from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
)

from .forms import DatasetUploadForm
from .models import Dataset


class DatasetUploadView(
    LoginRequiredMixin,
    CreateView
):

    model = Dataset

    form_class = DatasetUploadForm

    template_name = "datasets/upload.html"

    success_url = reverse_lazy(
        "datasets:list"
    )

    def form_valid(self, form):

        form.instance.user = self.request.user

        response = super().form_valid(form)

        from apps.profiling.services.profiling_service import (
            ProfilingService
        )

        ProfilingService.generate_profile(
            self.object
        )

        return response


class DatasetListView(
    LoginRequiredMixin,
    ListView
):

    model = Dataset

    template_name = "datasets/list.html"

    context_object_name = "datasets"

    def get_queryset(self):

        return Dataset.objects.filter(
            user=self.request.user
        )