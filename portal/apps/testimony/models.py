"""
This module contains the models for the testimony app.
"""
from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel
from wagtail.search import index


class Testimony(index.Indexed, UUIDModel):
    """
    Testimony model
    """
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    share = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_testimony"
        verbose_name = "Testimony"
        verbose_name_plural = "Testimonies"
        ordering = ["-created_at"]


auditlog.register(Testimony)
