import shutil
import tempfile
from datetime import timedelta

import pandas as pd
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.cleaning.forms import CleaningConfigForm
from apps.cleaning.models import CleaningJob, CleaningStatus
from apps.cleaning.services.cleaning_service import (
    CleaningService,
    parse_date,
)
from apps.datasets.models import Dataset


class DateEngineTests(TestCase):

    def test_auto_mode_parses_mixed_formats_and_preserves_invalid_values(self):
        dataframe = pd.DataFrame(
            {
                "event_date": [
                    "10/01/2024",
                    "02-16-2024",
                    "2024-03-21",
                    "not a date",
                    None,
                ]
            }
        )

        cleaned, summary = CleaningService.standardize_dates(
            dataframe,
            ["event_date"],
            parsing_mode="auto",
        )

        self.assertEqual(cleaned.loc[0, "event_date"], "2024-01-10")
        self.assertEqual(cleaned.loc[1, "event_date"], "2024-02-16")
        self.assertEqual(cleaned.loc[2, "event_date"], "2024-03-21")
        self.assertEqual(cleaned.loc[3, "event_date"], "not a date")
        self.assertTrue(pd.isna(cleaned.loc[4, "event_date"]))
        self.assertEqual(
            summary["date_parsing_statistics"]["event_date"],
            {
                "values_processed": 4,
                "values_parsed": 3,
                "invalid_values_preserved": 1,
            },
        )

    def test_explicit_date_mode_resolves_ambiguous_dates(self):
        self.assertEqual(
            parse_date("10/01/2024", parsing_mode="month_first"),
            "2024-10-01",
        )
        self.assertEqual(
            parse_date("10/01/2024", parsing_mode="day_first"),
            "2024-01-10",
        )


class CleaningConfigurationTests(TestCase):

    def test_date_parsing_mode_is_included_in_cleaning_config(self):
        form = CleaningConfigForm(
            {
                "standardize_dates": "on",
                "date_columns": ["event_date"],
                "date_parsing_mode": "month_first",
            },
            recommendations={
                "standardize_dates": {
                    "columns": ["event_date"],
                    "parsing_mode": "auto",
                }
            },
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.build_cleaning_config()["standardize_dates"]["parsing_mode"],
            "month_first",
        )


class CleaningWorkflowTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.media_directory = tempfile.mkdtemp()
        cls.settings_override = override_settings(MEDIA_ROOT=cls.media_directory)
        cls.settings_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.settings_override.disable()
        shutil.rmtree(cls.media_directory, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="owner",
            password="safe-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="other-user",
            password="safe-password",
        )
        self.dataset = Dataset.objects.create(
            user=self.user,
            name="Messy dates",
            original_file=SimpleUploadedFile(
                "messy_dates.csv",
                (
                    b"event_date,name,value\n"
                    b"10/01/2024,  jane doe ,10\n"
                    b"02-16-2024,JOHN DOE,20\n"
                    b"not a date,Jane Doe,20\n"
                    b"10/01/2024,  jane doe ,10\n"
                ),
                content_type="text/csv",
            ),
        )

    def test_cleaning_creates_csv_and_xlsx_downloads(self):
        job = CleaningService.run_cleaning(
            self.dataset,
            {
                "remove_duplicates": True,
                "handle_missing_values": False,
                "standardize_text": {"enabled": True, "columns": ["name"]},
                "standardize_dates": {
                    "enabled": True,
                    "columns": ["event_date"],
                    "parsing_mode": "auto",
                },
                "fix_data_types": {"enabled": False, "columns": []},
            },
        )

        self.assertEqual(job.status, "COMPLETED")
        self.assertTrue(job.cleaned_csv_file)
        self.assertTrue(job.cleaned_xlsx_file)
        self.assertEqual(job.rows_before, 4)
        self.assertEqual(job.rows_after, 3)
        self.assertEqual(
            job.cleaning_summary["date_parsing_statistics"]["event_date"][
                "invalid_values_preserved"
            ],
            1,
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse("cleaning:download", args=[job.id, "csv"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response["Content-Disposition"])

    def test_other_users_cannot_view_or_download_a_cleaning_job(self):
        job = CleaningService.run_cleaning(
            self.dataset,
            {
                "remove_duplicates": False,
                "handle_missing_values": False,
                "standardize_text": {"enabled": False, "columns": []},
                "standardize_dates": {"enabled": False, "columns": []},
                "fix_data_types": {"enabled": False, "columns": []},
            },
        )

        self.client.force_login(self.other_user)
        detail_response = self.client.get(reverse("cleaning:job_detail", args=[job.id]))
        download_response = self.client.get(
            reverse("cleaning:download", args=[job.id, "xlsx"])
        )

        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(download_response.status_code, 404)

    def test_cleaning_with_task_queue_eager(self):
        # Run Celery in eager mode so tasks execute synchronously during tests.
        from config.celery import app as celery_app

        prev = celery_app.conf.task_always_eager
        celery_app.conf.task_always_eager = True

        try:
            with override_settings(USE_TASK_QUEUE=True):
                job = CleaningService.run_cleaning(
                    self.dataset,
                    {
                        "remove_duplicates": True,
                        "handle_missing_values": False,
                        "standardize_text": {"enabled": True, "columns": ["name"]},
                        "standardize_dates": {
                            "enabled": True,
                            "columns": ["event_date"],
                            "parsing_mode": "auto",
                        },
                        "fix_data_types": {"enabled": False, "columns": []},
                    },
                )

                self.assertEqual(job.status, "COMPLETED")
                self.assertTrue(job.cleaned_csv_file)
                self.assertTrue(job.cleaned_xlsx_file)

        finally:
            celery_app.conf.task_always_eager = prev

    def test_history_shows_newest_cleaning_jobs_first(self):
        older_job = CleaningJob.objects.create(
            dataset=self.dataset,
            status=CleaningStatus.COMPLETED,
        )
        newer_job = CleaningJob.objects.create(
            dataset=self.dataset,
            status=CleaningStatus.COMPLETED,
        )
        now = timezone.now()
        CleaningJob.objects.filter(id=older_job.id).update(
            created_at=now - timedelta(days=1)
        )
        CleaningJob.objects.filter(id=newer_job.id).update(created_at=now)

        self.client.force_login(self.user)
        response = self.client.get(reverse("cleaning:history"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["jobs"][0].id, newer_job.id)
