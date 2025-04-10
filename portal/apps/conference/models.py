"""
This module contains the model for the conference app.
"""
from typing import Any

from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.search import index


class Conference(index.Indexed, UUIDModel, SoftDeletableModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.ForeignKey('location.Location', on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)
    instructors = models.ManyToManyField('instructor.Instructor', related_name="conference_instructors")

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "portal_conference"
        verbose_name = "Conference"
        verbose_name_plural = "Conferences"
        ordering = ["start_date"]

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


auditlog.register(Conference)
