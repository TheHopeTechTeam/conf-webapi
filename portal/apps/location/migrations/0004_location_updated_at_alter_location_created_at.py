# Generated by Django 5.2 on 2025-04-10 22:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_location_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='Update timestamp'),
        ),
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(db_comment='Creation timestamp', default=django.utils.timezone.now, editable=False),
        ),
    ]
