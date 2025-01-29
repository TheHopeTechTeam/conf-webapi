# Generated by Django 5.1.5 on 2025-01-28 22:49

import django.db.models.deletion
import model_utils.fields
import portal.apps.event_info.models
import uuid
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conference', '0002_conference_instructors'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSchedule',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sort_order', models.PositiveIntegerField(default=portal.apps.event_info.models.EventSchedule.count)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.conference')),
            ],
            options={
                'verbose_name': 'Event Schedule',
                'verbose_name_plural': 'Event Schedules',
                'db_table': 'portal_event_schedule',
                'ordering': ['sort_order'],
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
