# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-01 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feewaiver', '0010_auto_20201201_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='feewaiver',
            name='parks',
            field=models.ManyToManyField(to='feewaiver.Park'),
        ),
    ]