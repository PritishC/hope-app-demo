# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-15 17:33
from __future__ import unicode_literals

from django.db import migrations


def years(apps, schema_editor):
    Year = apps.get_model("job_ready", "Year")
    year_map = {
        'First Year': 1,
        'Second Year': 2,
        'Third Year': 3,
        'Fourth Year': 4,
    }

    for key, val in year_map.iteritems():
        Year.objects.filter(name=key).update(year_integer=val)


class Migration(migrations.Migration):
    
    dependencies = [
        ('job_ready', '0009_year_year_integer'),
    ]

    operations = [
    ]
