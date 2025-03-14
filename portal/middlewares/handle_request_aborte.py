"""
Middleware to handle request aborts
"""

from django.core.exceptions import RequestAborted
from django.core.handlers.asgi import ASGIRequest

from portal.libs.logger import logger


class HandleRequestAbortedMiddleware:
    """
    This middleware handles RequestAborted exceptions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: ASGIRequest):
        try:
            response = self.get_response(request)
            return response
        except RequestAborted:
            # Log the exception and suppress it
            logger.warning("Request was aborted by the client.")
            return
