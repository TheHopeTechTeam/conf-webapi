"""
This module contains the models for the language app.
"""
from auditlog.registry import auditlog
from django.db import models
from model_utils.models import UUIDModel
from wagtail.admin.panels import FieldPanel


class Language(UUIDModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    content_type = models.CharField(max_length=50)  # 模型名称
    object_id = models.UUIDField()  # 被翻译对象的 ID
    field_name = models.CharField(max_length=50)  # 被翻译字段名
    translated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel('language'),
        FieldPanel('content_type'),
        FieldPanel('object_id'),
        FieldPanel('field_name'),
        FieldPanel('translated_text'),
    ]

    def __str__(self):
        return f"{self.language.code} - {self.content_type} - {self.field_name}"

    class Meta:
        unique_together = ('content_type', 'object_id', 'language', 'field_name')
        db_table = "portal_translation"
        verbose_name = "Translation"
        verbose_name_plural = "Translations"

auditlog.register(Language)
auditlog.register(Translation)
