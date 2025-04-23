"""
This module contains the models for the feedback app.
"""
from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel
from wagtail.search import index

from portal.libs.consts.enums import FeedbackStatus


class Feedback(index.Indexed, UUIDModel):
    """
    Feedback model
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)
    remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=FeedbackStatus.choices(), default="Pending", db_comment="Feedback status")


    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_feedback"
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ["-created_at"]


auditlog.register(Feedback)
