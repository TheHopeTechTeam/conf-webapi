# Generated by Django 5.2 on 2025-04-10 22:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0003_conference_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='Update timestamp'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='created_at',
            field=models.DateTimeField(db_comment='Creation timestamp', default=django.utils.timezone.now, editable=False),
        ),
    ]
