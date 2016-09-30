from django.core.files.storage import Storage

from storages.backends.s3boto import S3BotoStorage
from proxy_storage.storages.base import (
    ProxyStorageBase,
    MultipleOriginalStoragesMixin
)
from proxy_storage.meta_backends.orm import ORMMetaBackend
from job_ready.models import ProxyStorageModel


class YoutubeStorage(Storage):
    """
    Storage class which implements only writing files to YouTube
    """
    # TODO: Write shit
    pass


class S3BotoOrYoutubeStorage(MultipleOriginalStoragesMixin,
                             ProxyStorageBase):
    """
    Proxy storage class for S3Boto or YoutubeStorages
    """
    # This storage class proxies for these original storages
    original_storages = (
        ('s3boto', S3BotoStorage()),
        ('youtube', YoutubeStorage()),
    )
    # Used to store meta-information about the info the storage class is handling
    # to the database. We have chosen the ORM mode of storing meta-info.
    meta_backend = ORMMetaBackend(
        model=ProxyStorageModel
    )

    def save(self, name, content, original_storage_path=None, using=None):
        if not using:
            # TODO: Fetch key value from Redis. The idea is that the key's
            # value will be set everytime on django admin save. This way,
            # I can customize which storage backend will be used to save shit.
            # More reliable than Django's in-memory cache, which will depend
            # on uWSGI's worker threads.
            pass
        return super(S3BotoOrYoutubeStorage, self).save(
            name=name,
            content=content,
            original_storage_path=original_storage_path,
            using=using
        )
