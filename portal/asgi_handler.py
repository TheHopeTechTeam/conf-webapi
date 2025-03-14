"""
Custom ASGI handler to suppress RequestAborted exceptions.
"""
import django
from django.core.exceptions import RequestAborted
from django.core.handlers.asgi import ASGIHandler

from portal.libs.logger import logger


class CustomASGIHandler(ASGIHandler):
    """
    Custom ASGI handler to suppress RequestAborted exceptions
    """

    async def handle(self, scope, receive, send):
        """

        :param scope:
        :param receive:
        :param send:
        :return:
        """
        try:
            return await super().handle(scope, receive, send)
        except RequestAborted:
            # logger.warning("RequestAborted exception suppressed in CustomASGIHandler.")  # 屏蔽並記錄
            return


def get_asgi_application():
    """
    The public interface to Django's ASGI support. Return an ASGI 3 callable.

    Avoids making django.core.handlers.ASGIHandler a public API, in case the
    internal implementation changes or moves in the future.
    """
    django.setup(set_prefix=False)
    return CustomASGIHandler()
