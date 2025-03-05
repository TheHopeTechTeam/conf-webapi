"""
FCM Device Handler
"""
from django.core.cache import BaseCache, cache


class FCMDeviceHandler:
    """
    FCM Device Handler
    """

    def __init__(self):
        self._cache: BaseCache = cache

    async def register_device(self, device_id: str, data: dict):
        """
        Register FCM Device
        """
        await self._cache.aset(key=f"fcm_device:{device_id}", value=data, timeout=60 * 60 * 24 * 30)
