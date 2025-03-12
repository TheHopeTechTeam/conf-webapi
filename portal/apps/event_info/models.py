"""
This module contains the models for the event_info app.
"""
from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel
from wagtail.admin.forms.account import _get_time_zone_choices
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
    time_zone = models.CharField(max_length=32, choices=_get_time_zone_choices(), default="Asia/Taipei")
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    sort_order = models.PositiveIntegerField(default=count)
    text_color = models.CharField(max_length=7, null=True, blank=True)
    background_color = models.CharField(max_length=7, null=True, blank=True)

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
