# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-30 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feewaiver', '0034_feewaivervisit_campgrounds'),
    ]

    operations = [
        migrations.AddField(
            model_name='feewaivervisit',
            name='index',
            field=models.IntegerField(null=True),
        ),
    ]
