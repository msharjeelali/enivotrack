import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied, NotFound

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        view = context.get("view")
        view_name = view.__class__.__name__ if view else "Unknown"

        if response.status_code >= 500:
            logger.error(f"API error in {view_name}: {exc}", exc_info=True)
        else:
            logger.warning(f"API error in {view_name}: {exc}")

        code = "error"
        if isinstance(exc, ValidationError):
            code = "validation_error"
        elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
            code = "authentication_failed"
        elif isinstance(exc, PermissionDenied):
            code = "permission_denied"
        elif isinstance(exc, NotFound):
            code = "not_found"

        detail = None
        data = response.data
        if isinstance(data, dict):
            if "detail" in data:
                detail = str(data.get("detail"))
            else:
                # Collapse field errors to the first message for consistent shape.
                for _, v in data.items():
                    if isinstance(v, list) and v:
                        detail = str(v[0])
                        break
                    if isinstance(v, str):
                        detail = v
                        break
                if not detail:
                    detail = "Validation error."
        elif isinstance(data, list) and data:
            detail = str(data[0])
        else:
            detail = str(data) if data is not None else "An error occurred."

        response.data = {"detail": detail, "code": code}
        return response

    logger.critical(f"Unhandled exception: {exc}", exc_info=True)
    return Response(
        {
            "detail": "Internal server error",
            "code": "internal_error",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )