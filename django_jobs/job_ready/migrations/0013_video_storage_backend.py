# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-31 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_ready', '0012_proxystoragemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='storage_backend',
            field=models.IntegerField(choices=[(0, 'AWS S3'), (1, 'YouTube')], default=0),
        ),
    ]