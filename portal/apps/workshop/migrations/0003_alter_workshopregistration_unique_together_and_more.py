# Generated by Django 5.1.3 on 2025-01-04 20:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_created_at'),
        ('workshop', '0002_workshop_participants_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='start_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workshop',
            name='end_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workshopregistration',
            name='workshop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workshop.workshop'),
        ),
        migrations.AlterUniqueTogether(
            name='workshopregistration',
            unique_together={('account', 'workshop')},
        ),
        migrations.RemoveField(
            model_name='workshopregistration',
            name='workshop_schedule',
        ),
        migrations.DeleteModel(
            name='WorkshopSchedule',
        ),
    ]
