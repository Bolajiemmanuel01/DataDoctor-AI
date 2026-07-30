import json
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.datasets.models import Dataset


class ApiCleaningTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="apiuser",
            password="safe-password",
        )

        self.dataset = Dataset.objects.create(
            user=self.user,
            name="API Messy",
            original_file=SimpleUploadedFile(
                "messy.csv",
                b"a,b\n1, x\n2, y\n",
                content_type="text/csv",
            ),
        )

    def test_clean_endpoint_creates_job_and_returns_status(self):

        self.client.force_login(self.user)

        url = f"/api/v1/datasets/{self.dataset.id}/clean/"

        response = self.client.post(url, data=json.dumps({}), content_type="application/json")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertTrue(payload.get("success"))

        job_id = payload.get("job_id")

        # Fetch job details
        detail_url = f"/api/v1/cleaning-jobs/{job_id}/"
        detail_response = self.client.get(detail_url)

        self.assertEqual(detail_response.status_code, 200)
        self.assertTrue(detail_response.json().get("success"))

    def test_profile_and_recommendations_and_download_endpoints(self):

        self.client.force_login(self.user)

        profile_url = f"/api/v1/datasets/{self.dataset.id}/profile/"
        profile_response = self.client.get(profile_url)

        # Initially profile may not exist depending on signals; expect 404 or success
        self.assertIn(profile_response.status_code, (200, 404))

        rec_url = f"/api/v1/datasets/{self.dataset.id}/recommendations/"
        rec_response = self.client.get(rec_url)

        self.assertEqual(rec_response.status_code, 200)
        self.assertTrue(rec_response.json().get("success"))

        download_url = f"/api/v1/datasets/{self.dataset.id}/download/"
        download_response = self.client.get(download_url)

        self.assertIn(download_response.status_code, (200, 404))
