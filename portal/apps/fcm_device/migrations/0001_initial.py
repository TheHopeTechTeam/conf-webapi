# Generated by Django 5.1.7 on 2025-03-31 22:34

import model_utils.fields
import uuid
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0008_alter_accountauthprovider_provider_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FCMDevice',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('device_id', models.CharField(max_length=255, unique=True)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('additional_data', models.JSONField(blank=True, null=True)),
                ('accounts', models.ManyToManyField(related_name='fcm_devices', to='account.account')),
            ],
            options={
                'verbose_name': 'FCM Device',
                'verbose_name_plural': 'FCM Devices',
                'db_table': 'portal_fcm_device',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
