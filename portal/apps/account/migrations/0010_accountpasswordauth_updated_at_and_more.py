# Generated by Django 5.2 on 2025-04-10 22:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_account_updated_at_accountauthprovider_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountpasswordauth',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='Update timestamp'),
        ),
        migrations.AlterField(
            model_name='account',
            name='created_at',
            field=models.DateTimeField(db_comment='Creation timestamp', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='Update timestamp'),
        ),
        migrations.AlterField(
            model_name='accountauthprovider',
            name='created_at',
            field=models.DateTimeField(db_comment='Creation timestamp', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='accountauthprovider',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='Update timestamp'),
        ),
        migrations.AlterField(
            model_name='accountpasswordauth',
            name='created_at',
            field=models.DateTimeField(db_comment='Creation timestamp', default=django.utils.timezone.now, editable=False),
        ),
    ]
