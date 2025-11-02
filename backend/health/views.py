from django.db import connection
from django.http import JsonResponse
from django.core.cache import cache


def health_check(request):
    """
    Health check endpoint with database and cache probes.
    Returns 200 if all services are healthy, 503 otherwise.
    """
    status_code = 200
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "cache": "unknown",
    }

    # Check database connectivity
    try:
        connection.ensure_connection()
        health_status["database"] = "healthy"
    except Exception as e:
        health_status["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
        status_code = 503

    # Check Redis/cache connectivity
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            health_status["cache"] = "healthy"
        else:
            health_status["cache"] = "unhealthy: cache not working"
            health_status["status"] = "degraded"
            status_code = 503
    except Exception as e:
        health_status["cache"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
        # Cache failure is not critical, so we keep 200 if DB is healthy
        if health_status["database"] == "healthy":
            status_code = 200

    return JsonResponse(health_status, status=status_code)

