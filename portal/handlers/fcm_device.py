"""
FCM Device Handler
"""
from django.core.cache import BaseCache, cache

from portal.serializers.v1.fcm_device import FCMCreate


class FCMDeviceHandler:
    """
    FCM Device Handler
    """

    def __init__(self):
        self._cache: BaseCache = cache

    async def register_device(self, device_id: str, fcm_create: FCMCreate):
        """
        Register FCM Device
        """
        await self._cache.aset(key=f"fcm_device:{device_id}", value=fcm_create.data, timeout=60 * 60 * 24 * 30)
