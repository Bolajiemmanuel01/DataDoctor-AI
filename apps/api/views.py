import json
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.datasets.models import Dataset
from apps.cleaning.services.recommendation_service import RecommendationService
from apps.cleaning.services.cleaning_service import CleaningService
from apps.cleaning.models import CleaningJob
from apps.profiling.models import DatasetProfile
from django.urls import reverse


@method_decorator(login_required, name="dispatch")
class CleanDatasetAPIView(View):
    """API endpoint to trigger cleaning for a dataset.

    POST body: JSON cleaning configuration object (optional). When omitted,
    recommended default actions will be selected automatically.
    """

    def post(self, request, dataset_id):

        dataset = get_object_or_404(
            Dataset, id=dataset_id, user=request.user
        )

        try:
            payload = json.loads(request.body.decode("utf-8")) if request.body else {}
        except Exception:
            return HttpResponseBadRequest("Invalid JSON payload")

        config = payload or {}

        # If no explicit config provided, generate defaults from recommendations
        if not config:
            recommendations = RecommendationService.generate_recommendations(dataset)
            # Build a simple config that enables recommended actions by default
            if recommendations.get("remove_duplicates", {}).get("recommended"):
                config["remove_duplicates"] = True
            if recommendations.get("handle_missing_values", {}).get("recommended"):
                config["handle_missing_values"] = True
            if recommendations.get("standardize_text"):
                config["standardize_text"] = {
                    "enabled": recommendations["standardize_text"].get("default_selected", False),
                    "columns": recommendations["standardize_text"].get("columns", []),
                }
            if recommendations.get("standardize_dates"):
                cfg = recommendations["standardize_dates"]
                config["standardize_dates"] = {
                    "enabled": cfg.get("default_selected", False),
                    "columns": cfg.get("columns", []),
                    "parsing_mode": cfg.get("parsing_mode", "auto"),
                    "day_first": cfg.get("day_first", True),
                }
            if recommendations.get("fix_data_types"):
                cfg = recommendations["fix_data_types"]
                config["fix_data_types"] = {
                    "enabled": cfg.get("default_selected", False),
                    "columns": cfg.get("columns", []),
                }

        try:
            # NOTE: This call is synchronous and will run the cleaning pipeline.
            job = CleaningService.run_cleaning(dataset, config)

            response = {
                "success": True,
                "job_id": str(job.id),
                "status": job.status,
            }

            return JsonResponse(response)

        except Exception as exc:
            return JsonResponse({"success": False, "error": str(exc)}, status=500)


@method_decorator(login_required, name="dispatch")
class CleaningJobDetailAPIView(View):

    def get(self, request, job_id):

        job = get_object_or_404(
            CleaningJob.objects.select_related("dataset"), id=job_id, dataset__user=request.user
        )

        data = {
            "id": str(job.id),
            "dataset_id": str(job.dataset.id),
            "status": job.status,
            "rows_before": job.rows_before,
            "rows_after": job.rows_after,
            "duplicates_removed": job.duplicates_removed,
            "cleaning_summary": job.cleaning_summary,
            "created_at": job.created_at.isoformat(),
        }

        return JsonResponse({"success": True, "job": data})


@method_decorator(login_required, name="dispatch")
class CancelCleaningJobAPIView(View):
    """Allow owners to cancel a pending or running cleaning job.

    This marks the job as CANCELLED. Long-running workers periodically
    check this flag and will stop early when set.
    """

    def post(self, request, job_id):

        job = get_object_or_404(
            CleaningJob.objects.select_related("dataset"), id=job_id, dataset__user=request.user
        )

        if job.status in ("COMPLETED", "FAILED", "CANCELLED"):
            return JsonResponse({"success": False, "error": "Job already finished"}, status=400)

        job.status = "CANCELLED"
        job.save(update_fields=["status"])

        # Also update dataset status for clarity
        dataset = job.dataset
        dataset.status = "CANCELLED"
        dataset.save(update_fields=["status", "updated_at"])

        return JsonResponse({"success": True, "job_id": str(job.id), "status": job.status})



@method_decorator(login_required, name="dispatch")
class DatasetProfileAPIView(View):

    def get(self, request, dataset_id):

        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

        profile = getattr(dataset, "profile", None)

        if not profile:
            return JsonResponse({"success": False, "error": "Profile not found"}, status=404)

        data = {
            "row_count": profile.row_count,
            "column_count": profile.column_count,
            "column_names": profile.column_names,
            "missing_values": profile.missing_values,
            "duplicate_rows": profile.duplicate_rows,
            "unique_value_summary": profile.unique_value_summary,
            "data_type_summary": profile.data_type_summary,
            "generated_at": profile.generated_at.isoformat(),
        }

        return JsonResponse({"success": True, "profile": data})



@method_decorator(login_required, name="dispatch")
class RecommendationsAPIView(View):

    def get(self, request, dataset_id):

        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

        recommendations = RecommendationService.generate_recommendations(dataset)

        return JsonResponse({"success": True, "recommendations": recommendations})



@method_decorator(login_required, name="dispatch")
class DatasetDownloadAPIView(View):

    def get(self, request, dataset_id):

        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

        job = (
            CleaningJob.objects.filter(dataset=dataset, status=CleaningJob._meta.get_field("status").choices and "COMPLETED" or "COMPLETED")
            .order_by("-created_at")
            .first()
        )

        if not job:
            return JsonResponse({"success": False, "error": "No completed cleaning job found"}, status=404)

        csv_url = f"/cleaning/job/{job.id}/download/csv/"
        xlsx_url = f"/cleaning/job/{job.id}/download/xlsx/"

        return JsonResponse({"success": True, "job_id": str(job.id), "csv_url": csv_url, "xlsx_url": xlsx_url})
