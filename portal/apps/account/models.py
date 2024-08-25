"""
Account model
"""
from django.db import models
from model_utils.models import UUIDModel
from wagtail.search import index


class Account(index.Indexed, UUIDModel):
    """
    Account model
    """
    google_uid = models.CharField(
        max_length=255,
        unique=True,
        db_comment="Google UID"
    )
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    auth_provider = models.CharField(max_length=10, choices=[('phone', 'Phone'), ('email', 'Email'), ('google', 'Google')], default='phone')
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, db_comment="Created at")
    last_login = models.DateTimeField(null=True, blank=True)
    app_name = models.CharField(max_length=128, default="DEFAULT")
    custom_claims = models.JSONField(blank=True, null=True)
    additional_info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.phone_number or self.email or self.google_uid

    class Meta:
        abstract = False
        db_table = "portal_account"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
