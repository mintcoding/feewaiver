# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-26 08:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationsLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.TextField(blank=True, verbose_name='To')),
                ('fromm', models.CharField(blank=True, max_length=200, verbose_name='From')),
                ('cc', models.TextField(blank=True, verbose_name='cc')),
                ('type', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone Call'), ('mail', 'Mail'), ('person', 'In Person'), ('onhold', 'On Hold'), ('onhold_remove', 'Remove On Hold'), ('with_qaofficer', 'With QA Officer'), ('with_qaofficer_completed', 'QA Officer Completed'), ('referral_complete', 'Referral Completed')], default='email', max_length=35)),
                ('reference', models.CharField(blank=True, max_length=100)),
                ('subject', models.CharField(blank=True, max_length=200, verbose_name='Subject / Description')),
                ('text', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Global Settings',
            },
        ),
        migrations.CreateModel(
            name='SystemMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'System maintenance',
            },
        ),
        migrations.CreateModel(
            name='UserSystemSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_row_per_park', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_settings', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name_plural': 'User System Settings',
            },
        ),
    ]
