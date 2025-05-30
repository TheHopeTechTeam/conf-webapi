# Generated by Django 5.2 on 2025-04-23 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_feedback_updated_at_alter_feedback_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[(0, 'Pending'), (1, 'Review'), (2, 'Discussion'), (3, 'Accepted'), (4, 'Done'), (5, 'Rejected'), (6, 'Archived')], db_comment='Feedback status', default='Pending', max_length=24),
        ),
    ]
