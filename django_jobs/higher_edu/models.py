from __future__ import unicode_literals

from django.db import models
from tinymce import models as tinymce_models


class University(models.Model):
    """
    Model for university description.
    """
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='university_logos')
    description = tinymce_models.HTMLField()
    short_description = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Universities'
