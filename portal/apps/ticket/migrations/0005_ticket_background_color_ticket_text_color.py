# Generated by Django 5.1.6 on 2025-03-04 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_ticketregisterdetail_order_person_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='background_color',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='text_color',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
