"""
This module contains the models for the event_info app.
"""
from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel
from wagtail.models import Orderable
from wagtail.search import index


class EventSchedule(index.Indexed, UUIDModel, Orderable):
    """
    Event Schedule model
    """
    def count():  # noqa
        return EventSchedule.objects.count() + 1

    conference = models.ForeignKey('conference.Conference', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    color = models.CharField(max_length=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sort_order = models.PositiveIntegerField(default=count)

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "portal_event_schedule"
        verbose_name = "Event Schedule"
        verbose_name_plural = "Event Schedules"
        ordering = ["sort_order"]


auditlog.register(EventSchedule)
