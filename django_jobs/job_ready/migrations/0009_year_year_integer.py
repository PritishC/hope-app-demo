# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-15 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_ready', '0008_auto_20160614_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='year_integer',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
