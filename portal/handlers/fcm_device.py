"""
FCM Device Handler
"""
from django.core.cache import BaseCache, cache

from sentry_sdk.tracing import Span
from portal.libs.decorators.sentry_tracer import distributed_trace
from portal.libs.logger import logger
from portal.serializers.v1.fcm_device import FCMCreate

from portal.apps.fcm_device.models import FCMDevice


class FCMDeviceHandler:
    """
    FCM Device Handler
    """

    def __init__(self):
        self._cache: BaseCache = cache

    @distributed_trace(inject_span=True)
    async def register_device(self, device_id: str, fcm_create: FCMCreate, _span: Span = None):
        """
        Register FCM Device
        """
        try:
            await FCMDevice.objects.aupdate_or_create(
                device_id=device_id,
                token=fcm_create.fcm_token,
                additional_data=fcm_create.additional_data,
            )
        except Exception as e:
            logger.warning(f"Error registering device: {e}")
            _span.set_data("device_id", device_id)
            _span.set_data("fcm_token", fcm_create.fcm_token)
            _span.set_data("error", str(e))
            _span.set_status("error")

