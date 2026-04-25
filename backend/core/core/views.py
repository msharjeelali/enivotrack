from django.db import connections
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(tags=["core"])
class HealthView(APIView):
    """
    Lightweight liveness/readiness endpoint.

    - Liveness: process is up and can serve requests.
    - Readiness: optionally checks DB connectivity (safe, no token exposure).
    """

    permission_classes = [AllowAny]

    def get(self, request):
        db_ok = True
        try:
            connections["default"].cursor().execute("SELECT 1")
        except Exception:
            db_ok = False

        status_str = "ok" if db_ok else "degraded"
        http_status = 200 if db_ok else 503

        return Response(
            {
                "status": status_str,
                "time": timezone.now().isoformat(),
                "checks": {"db": db_ok},
            },
            status=http_status,
        )

