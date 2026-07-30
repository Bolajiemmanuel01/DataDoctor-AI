from django.http import JsonResponse


def healthz(request):
    """Simple health check for load balancers and container healthchecks.

    Returns 200 OK with a small JSON payload when the app is up.
    """
    return JsonResponse({"status": "ok"})
