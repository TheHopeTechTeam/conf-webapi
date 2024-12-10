# Generated by Django 5.1.3 on 2024-12-10 22:25

import django.db.models.deletion
import model_utils.fields
import uuid
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_alter_account_created_at'),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Ticket Type',
                'verbose_name_plural': 'Ticket Types',
                'db_table': 'portal_ticket_type',
                'ordering': ['name'],
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.conference')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.tickettype')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'db_table': 'portal_ticket',
                'ordering': ['title'],
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='TicketRegisterDetail',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ticket_number', models.CharField(blank=True, max_length=128, null=True)),
                ('belong_church', models.CharField(blank=True, max_length=255, null=True)),
                ('identity', models.CharField(blank=True, choices=[('senior_pastor', '主任牧師'), ('pastor', '牧師'), ('evangelist', '傳道'), ('theology_student', '神學生'), ('ministry_leader', '事工負責人'), ('congregant', '會眾')], max_length=16, null=True)),
                ('registered_at', models.DateTimeField(blank=True, null=True)),
                ('unregistered_at', models.DateTimeField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket')),
            ],
            options={
                'verbose_name': 'Ticket Register Detail',
                'verbose_name_plural': 'Ticket Register Details',
                'db_table': 'portal_ticket_register_detail',
                'ordering': ['registered_at'],
                'unique_together': {('ticket', 'account')},
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]