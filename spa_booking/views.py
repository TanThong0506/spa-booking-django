import logging

from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            "status": "ok",
            "database": "connected"
        })

    except Exception as e:
        logger.exception("Health check failed")

        return JsonResponse({
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }, status=500)