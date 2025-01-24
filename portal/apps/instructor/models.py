"""
This module contains the models for the instructor app.
"""
from typing import Any

from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.images.models import Image


class Instructor(UUIDModel, SoftDeletableModel):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',  # Disables reverse relation to optimize database structure
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_instructor"
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"

    def delete(
        self,
        using: Any = None,
        *args: Any,
        soft: bool = True,
        **kwargs: Any
    ) -> tuple[int, dict[str, int]] | None:
        if soft:
            self.is_removed = True
            self.save()
            return 1, {}
        return super().delete(using=using, *args, **kwargs)


auditlog.register(Instructor)
