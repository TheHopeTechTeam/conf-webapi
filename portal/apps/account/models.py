"""
Account model
"""
from typing import Optional

from asgiref.sync import sync_to_async
from auditlog.registry import auditlog
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from model_utils.models import UUIDModel
from wagtail.search import index

from portal.libs.consts.enums import Provider


class Account(index.Indexed, UUIDModel):
    """
    Account model
    """
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number")]
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        validators=[EmailValidator(message="Enter a valid email address")]
    )
    display_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, db_comment="Creation timestamp", auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_service = models.BooleanField(default=False, db_comment="Is service")

    def __str__(self):
        return self.display_name or self.phone_number

    def delete(
        self,
        using=None,
        *args,
        soft=True,
        **kwargs
    ) -> Optional[tuple[int, dict[str, int]]]:
        if soft:
            self.is_active = False
            self.save()
            return 1, {}
        return super().delete(using=using, *args, **kwargs)

    async def adelete(
        self,
        using=None,
        *args,
        soft=True,
        **kwargs
    ) -> Optional[tuple[int, dict[str, int]]]:
        """

        :param using:
        :param args:
        :param soft:
        :param kwargs:
        :return:
        """
        return await sync_to_async(self.delete)(
            using=using,
            *args,
            soft=soft,
            **kwargs
        )

    class Meta:
        abstract = False
        db_table = "portal_account"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["email"]),
        ]


class AccountAuthProvider(index.Indexed, UUIDModel):
    """
    AccountAuthProvider model
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    provider = models.CharField(max_length=16, choices=Provider.choices)
    provider_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, db_comment="Creation timestamp", auto_now_add=True)
    extra_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.provider} - {self.account.display_name or self.account.phone_number}"

    class Meta:
        abstract = False
        db_table = "portal_account_auth_provider"
        verbose_name = "AccountAuthProvider"
        verbose_name_plural = "AccountAuthProviders"


class AccountPasswordAuth(index.Indexed, UUIDModel):
    """
    AccountPasswordAuth model
    """
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False, db_comment="Creation timestamp", auto_now_add=True)

    def __str__(self):
        return self.account.display_name or self.account.phone_number

    class Meta:
        abstract = False
        db_table = "portal_account_password_auth"
        verbose_name = "AccountPasswordAuth"
        verbose_name_plural = "AccountPasswordAuths"


auditlog.register(Account)
