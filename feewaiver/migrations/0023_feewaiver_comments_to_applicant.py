# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-14 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feewaiver', '0022_auto_20201211_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='feewaiver',
            name='comments_to_applicant',
            field=models.TextField(blank=True),
        ),
    ]
