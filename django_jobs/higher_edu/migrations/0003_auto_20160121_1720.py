# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('higher_edu', '0002_auto_20160121_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='short_description',
            field=models.CharField(max_length=100),
        ),
    ]
