import os
from celery import Celery
from django.conf import settings

# Use the Django settings module for Celery configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("datadoctor")

# Read broker config from Django settings
app.conf.broker_url = getattr(settings, "CELERY_BROKER_URL", "redis://redis:6379/0")
app.conf.result_backend = getattr(settings, "CELERY_RESULT_BACKEND", app.conf.broker_url)

# Auto-discover tasks in installed apps
app.autodiscover_tasks()
