"""
FileHandler
"""
from datetime import timedelta
from typing import Optional

from django.conf import settings
from django.core.cache import BaseCache, cache
from firebase_admin import storage
from google.cloud.storage import Bucket, Blob
from wagtail.images.models import Image

from portal.libs.consts import cache_keys


class FileHandler:
    """FileHandler"""

    def __init__(self):
        self._cache: BaseCache = cache

    async def get_file_url(self, image_id: int) -> Optional[str]:
        """
        :param image_id:
        :return:
        """
        cache_key = cache_keys.get_firebase_signed_url_key(image_id)
        if value := await self._cache.aget(cache_key):
            return value
        try:
            image: Image = await Image.objects.aget(id=image_id)
        except Image.DoesNotExist:
            return None
        bucket: Bucket = storage.bucket()
        blob: Blob = bucket.get_blob(f"{settings.FIREBASE_STORAGE_LOCATION}/{image.file.name}")
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(hours=1),
        )
        await self._cache.aset(
            key=cache_key,
            value=signed_url,
            timeout=60 * 60
        )
        return signed_url
