"""
FileHandler
"""
from typing import Optional

import boto3
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.cache import BaseCache, cache
from wagtail.images.models import Image

from portal.libs.consts import cache_keys


class FileHandler:
    """FileHandler"""

    def __init__(self):
        self._cache: BaseCache = cache
        self._s3_client = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)

    async def get_file_url(self, image_id: int, rendition: str = "original") -> Optional[str]:
        """
        :param image_id:
        :param rendition:
        :return:
        """
        cache_key = cache_keys.get_firebase_signed_url_key(image_id)
        if value := await self._cache.aget(cache_key):
            return value
        try:
            image: Image = await Image.objects.aget(id=image_id)
            image_rendition = await sync_to_async(image.get_rendition)(rendition)
        except Image.DoesNotExist:
            return None

        signed_url = image_rendition.url

        await self._cache.aset(
            key=cache_key,
            value=signed_url,
            timeout=60 * 60
        )
        return signed_url
