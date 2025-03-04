"""
EventInfoHandler
"""
import uuid
from collections import defaultdict

from portal.apps.event_info.models import EventSchedule

from portal.serializers.v1.event_info import EventScheduleBase, EventScheduleItem, EventScheduleList


class EventInfoHandler:
    """EventInfoHandler"""

    def __init__(self):
        pass

    async def get_event_schedule(self, conference_id: uuid.UUID) -> EventScheduleList:
        """
        Get event schedule
        :return:
        """
        event_schedule_item_list = []
        event_schedule_map = defaultdict(list)
        event_schedules = (
            EventSchedule.objects
            .filter(conference_id=conference_id)
            .order_by("start_time")
        )
        async for event_schedule in event_schedules:
            event_schedule_map[event_schedule.start_time.date()].append(
                EventScheduleBase(
                    id=event_schedule.id,
                    title=event_schedule.title,
                    description=event_schedule.description,
                    start_time=event_schedule.start_time,
                    background_color=event_schedule.background_color
                )
            )
        for start_time, schedules in event_schedule_map.items():
            event_schedule_item_list.append(
                EventScheduleItem(
                    date=start_time,
                    weekday=start_time.strftime("%a"),
                    schedules=schedules
                )
            )

        return EventScheduleList(schedules=event_schedule_item_list)
