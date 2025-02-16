"""
EventInfoHandler
"""
import uuid

from portal.apps.event_info.models import EventSchedule

from portal.serializers.v1.event_info import EventScheduleBase, EventScheduleList


class EventInfoHandler:
    """EventInfoHandler"""

    def __init__(self):
        pass

    async def get_event_schedule(self, conference_id: uuid.UUID) -> EventScheduleList:
        """
        Get event schedule
        :return:
        """
        event_schedule_list = []
        event_schedules = (
            EventSchedule.objects
            .filter(conference_id=conference_id)
            .order_by("start_time")
        )
        async for event_schedule in event_schedules:
            event_schedule_list.append(
                EventScheduleBase(
                    id=event_schedule.id,
                    title=event_schedule.title,
                    description=event_schedule.description,
                    start_time=event_schedule.start_time,
                    color=event_schedule.color
                )
            )
        return EventScheduleList(schedules=event_schedule_list)
