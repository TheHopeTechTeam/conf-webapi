from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging
from firebase_admin.messaging import SendResponse
from sentry_sdk.tracing import Span

from portal.apps.fcm_device.models import FCMDevice
from portal.libs.consts.enums import NotificationType, NotificationStatus, NotificationHistoryStatus
from portal.libs.decorators.sentry_tracer import distributed_trace
from ..models import Notification, NotificationHistory


@receiver(post_save, sender=Notification)
@distributed_trace(inject_span=True)
def notification_post_save(sender: ModelBase, instance: Notification, created: bool, _span: Span, **kwargs):
    """
    Signal to handle notification post save
    :param sender:
    :param instance:
    :param created:
    :param _span:
    :param kwargs:
    :return:
    """
    if created:
        try:
            result = None
            tokens = []
            if instance.type == NotificationType.MULTIPLE.value:
                # Handle the notification creation logic here
                notification_histories = []
                fcm_objs = FCMDevice.objects.filter(token__isnull=False)
                for fcm_obj in fcm_objs:
                    tokens.append(fcm_obj.token)
                    notification_histories.append(
                        NotificationHistory(
                            notification=instance,
                            device=fcm_obj,
                            status=NotificationStatus.PENDING.value
                        )
                    )

                NotificationHistory.objects.bulk_create(notification_histories)

                multicast_message = messaging.MulticastMessage(
                    notification=messaging.Notification(
                        title=instance.title,
                        body=instance.message,
                    ),
                    data={
                        "notification_id": str(instance.id),
                        "type": str(instance.type)
                    },
                    tokens=tokens
                )
                result = messaging.send_each_for_multicast(multicast_message=multicast_message)
                instance.status = NotificationStatus.SENT.value
                instance.save()
        except Exception as exc:
            # Handle the exception here
            instance.status = NotificationStatus.FAILED.value
            instance.save()
        else:
            if result:
                instance.success_count = result.success_count
                instance.failure_count = result.failure_count
                instance.save()
                for index, response in enumerate(result.responses):  # type: (int, SendResponse)
                    if response.success:
                        filtered_device = FCMDevice.objects.filter(token=tokens[index]).first()
                        NotificationHistory.objects.filter(
                            notification=instance,
                            device=filtered_device
                        ).update(
                            message_id=response.message_id,
                            status=NotificationHistoryStatus.SUCCESS.value,
                            exception=None
                        )
                    else:
                        filtered_device = FCMDevice.objects.filter(token=tokens[index]).first()
                        NotificationHistory.objects.filter(
                            notification=instance,
                            device=filtered_device
                        ).update(
                            message_id=None,
                            status=NotificationHistoryStatus.FAILED.value,
                            exception=response.exception
                        )
    else:
        # Handle the notification update logic here
        pass
