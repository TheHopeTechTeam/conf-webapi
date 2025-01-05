"""
This module contains the models for the workshop app.
"""
from typing import Any

from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.admin.forms.account import _get_time_zone_choices  # noqa
from wagtail.search import index


class Workshop(index.Indexed, UUIDModel, SoftDeletableModel):

    title = models.CharField(max_length=255)
    description = models.TextField()
    conference = models.ForeignKey('conference.Conference', on_delete=models.CASCADE)
    location = models.ForeignKey('location.Location', on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey('instructor.Instructor', on_delete=models.SET_NULL, null=True)
    participants_limit = models.PositiveBigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    time_zone = models.CharField(max_length=32, choices=_get_time_zone_choices(), default="Asia/Taipei")
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "portal_workshop"
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"
        ordering = ["title"]

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


class WorkshopRegistration(index.Indexed, UUIDModel, SoftDeletableModel):
    workshop = models.ForeignKey(Workshop, null=True, on_delete=models.CASCADE)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    unregistered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.account.display_name} - {self.workshop.title}"

    class Meta:
        db_table = "portal_workshop_registration"
        verbose_name = "Workshop Registration"
        verbose_name_plural = "Workshop Registrations"
        ordering = ["registered_at"]
        unique_together = ('account', 'workshop')

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

auditlog.register(Workshop)
