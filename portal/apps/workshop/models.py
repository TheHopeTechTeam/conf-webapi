"""
This module contains the models for the workshop app.
"""
from typing import Any

from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.search import index


class Workshop(index.Indexed, UUIDModel, SoftDeletableModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    conference = models.ForeignKey('conference.Conference', on_delete=models.CASCADE)
    location = models.ForeignKey('location.Location', on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey('instructor.Instructor', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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


class WorkshopSchedule(UUIDModel):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.workshop.title} - {self.start_datetime}"

    class Meta:
        db_table = "portal_workshop_schedule"
        verbose_name = "Workshop Schedule"
        verbose_name_plural = "Workshop Schedules"
        ordering = ["start_datetime"]


class WorkshopRegistration(index.Indexed, UUIDModel, SoftDeletableModel):
    workshop_schedule = models.ForeignKey(WorkshopSchedule, on_delete=models.CASCADE)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    unregistered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.account.display_name} - {self.workshop_schedule.workshop.title}"

    class Meta:
        db_table = "portal_workshop_registration"
        verbose_name = "Workshop Registration"
        verbose_name_plural = "Workshop Registrations"
        ordering = ["registered_at"]
        unique_together = ('account', 'workshop_schedule')

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
