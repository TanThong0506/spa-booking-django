import logging

from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    """Log API errors and return DRF's standard error response."""
    response = exception_handler(exc, context)

    view_name = context.get('view').__class__.__name__ if context.get('view') else 'UnknownView'
    request = context.get('request')
    request_path = request.path if request else 'unknown-path'
    method = request.method if request else 'UNKNOWN'

    if response is None:
        logger.exception(
            'Unhandled API exception in %s %s (%s)',
            method,
            request_path,
            view_name,
            exc_info=exc,
        )
        return response

    if response.status_code >= 500:
        logger.exception(
            'API server error %s in %s %s (%s): %s',
            response.status_code,
            method,
            request_path,
            view_name,
            response.data,
            exc_info=exc,
        )
    elif response.status_code >= 400:
        logger.warning(
            'API client error %s in %s %s (%s): %s',
            response.status_code,
            method,
            request_path,
            view_name,
            response.data,
        )

    return response
