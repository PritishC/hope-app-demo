# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-10 12:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('icon', models.CharField(blank=True, help_text='Icon to display for this list item on the app - enter names from ionicons.com or leave blank', max_length=25)),
                ('article_content', tinymce.models.HTMLField(max_length=4000)),
                ('added_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_description', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('icon', models.CharField(blank=True, help_text='Icon to display for this list item on the app - enter names from ionicons.com or leave blank', max_length=25)),
                ('video_file', models.FileField(upload_to='videos')),
                ('added_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='job_ready.Category')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='job_ready.Category'),
        ),
    ]
