# Generated by Django 5.1.3 on 2024-11-26 20:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator(message='Enter a valid email address')]),
        ),
    ]
