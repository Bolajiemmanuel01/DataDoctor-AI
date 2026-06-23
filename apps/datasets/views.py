from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
)
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.profiling.models import DatasetProfile
from apps.cleaning.services.recommendation_service import (
    RecommendationService
)
from apps.cleaning.forms import CleaningConfigForm
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

class DatasetProfileView(
    LoginRequiredMixin,
    TemplateView
):

    template_name = "datasets/profile.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        dataset = get_object_or_404(
            Dataset,
            id=self.kwargs["dataset_id"],
            user=self.request.user
        )

        recommendations = (
            RecommendationService.generate_recommendations(
                dataset
            )
        )

        context["recommendations"] = recommendations

        context["cleaning_form"] = CleaningConfigForm(
            recommendations=recommendations
        )

        profile = getattr(
            dataset,
            "profile",
            None
        )

        context["dataset"] = dataset
        context["profile"] = profile

        return context