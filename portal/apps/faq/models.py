"""
This module contains the models for the FAQ app.
"""
from django.db import models
from auditlog.registry import auditlog
from django.utils import timezone

from model_utils.models import UUIDModel, SoftDeletableModel
from wagtail.models import Orderable


class FaqCategory(UUIDModel, SoftDeletableModel, Orderable):
    def count():  # noqa
        return FaqCategory.objects.count() + 1

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)
    sort_order = models.PositiveIntegerField(default=count)

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_faq_category"
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        ordering = ["sort_order"]


class Faq(UUIDModel, SoftDeletableModel, Orderable):
    def count():  # noqa
        return Faq.objects.count() + 1

    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    related_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_comment="Creation timestamp")
    updated_at = models.DateTimeField(editable=False, db_comment="Update timestamp", auto_now=True)
    sort_order = models.PositiveIntegerField(default=count)

    @property
    def pk(self) -> str:
        """

        :return:
        """
        return str(self.id)

    def __str__(self):
        return self.question

    class Meta:
        db_table = "portal_faq"
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["sort_order"]


auditlog.register(FaqCategory)
auditlog.register(Faq)
