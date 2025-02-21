"""
This module contains the models for the location app.
"""
from typing import Any

from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.images.models import Image
from wagtail.search import index


class Location(index.Indexed, UUIDModel, SoftDeletableModel):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',  # Disables reverse relation to optimize database structure
    )

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["name"]


auditlog.register(Location)
