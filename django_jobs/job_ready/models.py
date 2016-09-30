from __future__ import unicode_literals
from boto.s3.connection import S3Connection
from proxy_storage.meta_backends.orm import ProxyStorageModelBase

from django.conf import settings
from django.db import models
from tinymce import models as tinymce_models

from django_jobs.settings import AUTH_USER_MODEL


class ProxyStorageModel(ProxyStorageModelBase):
    """
    Model class for the meta-backend used by the custom
    storage backend.
    """
    pass


class Content(models.Model):
    """
    Abstract class for all kinds of content
    on the mobile app.
    """
    title = models.CharField(max_length=50)
    added_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(AUTH_USER_MODEL,
                                    null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('job_ready.Category')
    icon = models.CharField(max_length=25, blank=True,
                            help_text="Icon to display for this list"
                                      " item on the app - enter names"
                                      " from ionicons.com or leave blank")
    is_premium = models.BooleanField(default=True,
                                     help_text="Whether this content can only"
                                               " be viewed by subscribed users")

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.title

    def get_s3_connection(self):
        try:
            return S3Connection(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        except:
            pass


class Category(models.Model):
    """
    Model for categorization of content. On the app,
    content will show under these categories as lists.
    """
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=500)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return u"%s" % self.name


class Year(Category):
    """
    Represents what year of college the user is in.
    Also used to categorize content according to
    what year the user is in.

    Is essentially a special kind of Category.
    """
    year_integer = models.PositiveIntegerField()

    class Meta:
        ordering = ('year_integer',)


class Video(Content):
    """
    Model for video content.
    """
    S3 = 0
    YOUTUBE = 1

    STORAGE_BACKENDS = (
        (S3, "AWS S3"),
        (YOUTUBE, "YouTube"),
    )

    video_file = models.FileField(upload_to='videos')
    description = tinymce_models.HTMLField()
    year = models.ManyToManyField('job_ready.Year', null=True,
                                  related_name='videos')
    storage_backend = models.IntegerField(choices=STORAGE_BACKENDS,
                                          default=S3)

    class Meta:
        ordering = ('title',)

    def generate_url(self):
        """
        Generate a pre-signed URL which lasts a week.
        """
        conn = self.get_s3_connection()

        if not conn:
            return self.video_file.url

        return conn.generate_url(
            7 * 24 * 60 * 60,  # timeout
            'GET',
            settings.AWS_STORAGE_BUCKET_NAME,
            self.video_file.name
        )

class Article(Content):
    """
    Model for article content.
    """
    article_content = tinymce_models.HTMLField()
    year = models.ManyToManyField('job_ready.Year', null=True,
                                  related_name='articles')

    class Meta:
        ordering = ('title',)
