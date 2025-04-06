"""
Notification model
"""
from django.db import models
from model_utils.models import UUIDModel
from wagtail.search import index

from portal.libs.consts.enums import NotificationType, NotificationStatus, NotificationHistoryStatus
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging
from sentry_sdk.tracing import Span

from portal.apps.fcm_device.models import FCMDevice
from portal.libs.consts.enums import NotificationType


class Notification(index.Indexed, UUIDModel):
    """
    Notification model
    """
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.PositiveSmallIntegerField(choices=NotificationType.choices())
    status = models.PositiveSmallIntegerField(choices=NotificationStatus.choices(), default=NotificationStatus.PENDING.value)
    created_at = models.DateTimeField(auto_now_add=True)
    failure_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

    class Meta:
        db_table = "portal_notification"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


class NotificationHistory(UUIDModel):
    """
    Notification history model
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="history")
    device = models.ForeignKey(FCMDevice, on_delete=models.CASCADE, related_name="notification_history")
    message_id = models.CharField(max_length=255, blank=True, null=True)
    exception = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=NotificationHistoryStatus.choices())
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification.title} - {self.device.device_id} - {self.status}"


    class Meta:
        db_table = "portal_notification_history"
        verbose_name = "Notification History"
        verbose_name_plural = "Notification Histories"
        unique_together = ("notification", "device")
