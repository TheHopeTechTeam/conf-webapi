"""
This module contains the models for the location app.
"""
from typing import Any

from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.search import index


class Location(index.Indexed, UUIDModel, SoftDeletableModel):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["name"]

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

auditlog.register(Location)
