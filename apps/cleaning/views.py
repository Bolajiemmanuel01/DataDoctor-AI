from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.views.generic import DetailView, ListView, View

from .models import CleaningJob


class CleaningJobDetailView(LoginRequiredMixin, DetailView):

    model = CleaningJob

    template_name = "cleaning/detail.html"

    context_object_name = "job"

    pk_url_kwarg = "job_id"

    def get_queryset(self):
        return CleaningJob.objects.select_related("dataset").filter(
            dataset__user=self.request.user
        )


class CleaningHistoryListView(LoginRequiredMixin, ListView):

    template_name = "cleaning/history.html"
    context_object_name = "jobs"
    paginate_by = 20

    def get_queryset(self):
        return CleaningJob.objects.select_related("dataset").filter(
            dataset__user=self.request.user
        )


class DownloadCleanedDatasetView(LoginRequiredMixin, View):

    def get(self, request, job_id, file_format):
        job = get_object_or_404(
            CleaningJob.objects.select_related("dataset"),
            id=job_id,
            dataset__user=request.user,
        )

        files = {
            "csv": job.cleaned_csv_file or job.cleaned_file,
            "xlsx": job.cleaned_xlsx_file,
        }
        cleaned_file = files.get(file_format)

        if not cleaned_file:
            raise Http404("The requested cleaned file is not available.")

        filename = f"{job.dataset.name}_cleaned.{file_format}"
        return FileResponse(
            cleaned_file.open("rb"),
            as_attachment=True,
            filename=filename,
        )
