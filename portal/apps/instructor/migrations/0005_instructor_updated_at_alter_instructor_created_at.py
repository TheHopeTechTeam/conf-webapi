# Generated by Django 5.2 on 2025-04-10 22:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0004_alter_instructor_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='Update timestamp'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='created_at',
            field=models.DateTimeField(db_comment='Creation timestamp', default=django.utils.timezone.now, editable=False),
        ),
    ]
