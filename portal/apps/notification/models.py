"""
Notification model
"""
from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel
from wagtail.search import index

from portal.apps.fcm_device.models import FCMDevice
from portal.libs.consts.enums import NotificationStatus, NotificationHistoryStatus
from portal.libs.consts.enums import NotificationType


class Notification(index.Indexed, UUIDModel):
    """
    Notification model
    """
    title = models.CharField(max_length=255)
    message = models.TextField()
    url = models.URLField(blank=True, null=True)
    type = models.PositiveSmallIntegerField(choices=NotificationType.choices())
    status = models.PositiveSmallIntegerField(choices=NotificationStatus.choices(), default=NotificationStatus.PENDING.value)
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)
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
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)

    def __str__(self):
        return f"{self.notification.title} - {self.device.device_id} - {self.status}"


    class Meta:
        db_table = "portal_notification_history"
        verbose_name = "Notification History"
        verbose_name_plural = "Notification Histories"
        unique_together = ("notification", "device")


auditlog.register(Notification)
auditlog.register(NotificationHistory)
