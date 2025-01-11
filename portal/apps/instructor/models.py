"""
This module contains the models for the instructor app.
"""
from typing import Any, Optional

from auditlog.registry import auditlog
from django.conf import settings
from django.db import models
from firebase_admin import storage
from google.cloud.storage import Bucket
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

    async def get_image_url(self) -> Optional[str]:
        """

        :return:
        """
        if self.image_id:
            image: Image = await Image.objects.aget(id=self.image_id)
            bucket: Bucket = storage.bucket()
            blob = bucket.get_blob(f"{settings.FIREBASE_STORAGE_LOCATION}/{image.file.name}")
            return blob.public_url
        return None

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
