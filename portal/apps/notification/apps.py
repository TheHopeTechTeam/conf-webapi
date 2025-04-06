"""
Django App Configuration for Notification Module
"""
from django.apps import AppConfig


class NotificationConfig(AppConfig):
    """
    Configuration class for the Notification app.
    """
    name = "portal.apps.notification"

    def ready(self):
        """
        Import the signals module to ensure that the signals are registered
        when the app is ready.
        """
        import portal.apps.notification.signals  # noqa
