"""
FileHandler
"""
from datetime import timedelta
from typing import Optional

import boto3
from django.conf import settings
from django.core.cache import BaseCache, cache

from wagtail.images.models import Image

from portal.libs.consts import cache_keys


class FileHandler:
    """FileHandler"""

    def __init__(self):
        self._cache: BaseCache = cache
        self._s3_client = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)

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

        signed_url = self._s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': f"{settings.ENV.lower()}/{image.file.name}"
            },
            ExpiresIn=timedelta(hours=1).seconds
        )

        await self._cache.aset(
            key=cache_key,
            value=signed_url,
            timeout=60 * 60
        )
        return signed_url
