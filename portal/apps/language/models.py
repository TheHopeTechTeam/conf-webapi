"""
This module contains the models for the language app.
"""
from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel
from wagtail.admin.panels import FieldPanel


class Language(UUIDModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_language"
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super().save(*args, **kwargs)


class Translation(UUIDModel):
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name='translations'
    )
    content_type = models.CharField(max_length=50)
    object_id = models.UUIDField()
    field_name = models.CharField(max_length=50)
    translated_text = models.TextField()
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return f"{self.language.code} - {self.content_type} - {self.field_name}"

    class Meta:
        unique_together = ('content_type', 'object_id', 'language', 'field_name')
        db_table = "portal_translation"
        verbose_name = "Translation"
        verbose_name_plural = "Translations"


auditlog.register(Language)
auditlog.register(Translation)
