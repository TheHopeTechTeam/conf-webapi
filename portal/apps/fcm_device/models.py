"""
FCM Device model
"""
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel
from wagtail.search import index


class FCMDevice(index.Indexed, UUIDModel):
    """
    FCM Device model
    """
    device_id = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255, unique=True)
    additional_data = models.JSONField(blank=True, null=True)
    accounts = models.ManyToManyField("account.Account", related_name="fcm_devices")
    created_at = models.DateTimeField(
        editable=False,
        default=timezone.now,
        db_comment="Creation timestamp"
    )
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)

    def __str__(self):
        return self.device_id

    class Meta:
        db_table = "portal_fcm_device"
        verbose_name = "FCM Device"
        verbose_name_plural = "FCM Devices"
        unique_together = ("device_id", "token")
