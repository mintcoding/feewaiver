# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-16 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feewaiver', '0024_feewaivervisit_camping_assessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='feewaivervisit',
            name='issued',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='feewaiver',
            name='processing_status',
            field=models.CharField(choices=[('with_assessor', 'With Assessor'), ('with_approver', 'With Approver'), ('issued', 'Issued'), ('declined', 'Declined')], default='with_assessor', max_length=30, verbose_name='Processing Status'),
        ),
    ]
