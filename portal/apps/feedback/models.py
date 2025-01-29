"""
This module contains the models for the feedback app.
"""
from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel
from wagtail.search import index


class Feedback(index.Indexed, UUIDModel):
    """
    Feedback model
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_feedback"
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ["-created_at"]


auditlog.register(Feedback)
