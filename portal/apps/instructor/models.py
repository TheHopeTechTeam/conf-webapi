"""
This module contains the models for the instructor app.
"""
from typing import Any

from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.models import Orderable
from wagtail.images.models import Image


class Instructor(UUIDModel, SoftDeletableModel, Orderable):
    """
    Instructor model
    """
    def count():  # noqa
        return Instructor.objects.count() + 1

    name = models.CharField(max_length=255)
    title = models.CharField(null=True, blank=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',  # Disables reverse relation to optimize database structure
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sort_order = models.PositiveIntegerField(default=count)

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_instructor"
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"
        ordering = ["sort_order"]


auditlog.register(Instructor)
