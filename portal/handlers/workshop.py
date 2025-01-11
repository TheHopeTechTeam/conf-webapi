"""
WorkshopHandler
"""
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil import parser
from django.core.cache import BaseCache, cache

from portal.apps.account.models import Account
from portal.apps.instructor.models import Instructor
from portal.apps.location.models import Location
from portal.apps.workshop.models import WorkshopTimeSlot, Workshop, WorkshopRegistration
from portal.exceptions.api_base import APIException
from portal.libs.contexts.api_context import APIContext, get_api_context
from portal.serializers.v1.instructor import InstructorBase
from portal.serializers.v1.location import LocationBase
from portal.serializers.v1.workshop import WorkshopList, WorkshopBase, WorkshopDetail


class WorkshopHandler:
    """WorkshopHandler"""

    def __init__(self):
        try:
            self._api_context: APIContext = get_api_context()
        except Exception:
            self._api_context = None
        self._cache: BaseCache = cache

    async def get_workshop_schedules(self) -> dict:
        """
        Get the workshop list

        :return:
        """
        workshop_schedule = {}
        workshop_time_slots = WorkshopTimeSlot.objects.filter(
            is_removed=False,
            start_datetime__gte=parser.parse("2025-05-01T16:00:00Z"),  # temporary hard-coded date
            end_datetime__lte=parser.parse("2025-05-03T16:00:00Z")  # temporary hard-coded date
        ).all()
        workshop_time_slot_ids = [workshop_time_slot.id async for workshop_time_slot in workshop_time_slots]
        workshops = Workshop.objects.filter(
            time_slot_id__in=workshop_time_slot_ids,
            is_removed=False
        ).all()
        async for workshop in workshops:
            time_slot_obj: WorkshopTimeSlot = await WorkshopTimeSlot.objects.aget(id=workshop.time_slot_id)  # type: ignore
            location: Location = await Location.objects.aget(id=workshop.location_id)  # type: ignore
            start_datetime_with_tz = time_slot_obj.start_datetime.astimezone(tz=ZoneInfo(time_slot_obj.time_zone))
            end_datetime_with_tz = time_slot_obj.end_datetime.astimezone(tz=ZoneInfo(time_slot_obj.time_zone))
            start_date = start_datetime_with_tz.strftime("%Y%m%d")
            start_time = start_datetime_with_tz.strftime("%H%M")
            if start_date not in workshop_schedule:
                workshop_schedule[start_date] = {}
            if start_time not in workshop_schedule[start_date]:
                workshop_schedule[start_date][start_time] = []
            workshop_schedule[start_date][start_time].append(
                WorkshopBase(
                    id=workshop.id,
                    title=workshop.title,
                    description=workshop.description,
                    location=LocationBase(
                        id=location.id,
                        name=location.name,
                        address=location.address,
                        floor=location.floor,
                        room_number=location.room_number
                    ),
                    start_datetime=start_datetime_with_tz,
                    end_datetime=end_datetime_with_tz
                )
            )
        return workshop_schedule

    async def get_workshop_detail(self, workshop_id: uuid.UUID) -> WorkshopDetail:
        """
        Get workshop detail

        :param workshop_id:
        :return:
        """
        workshop: Workshop = await Workshop.objects.aget(id=workshop_id)
        time_slot_obj: WorkshopTimeSlot = await WorkshopTimeSlot.objects.aget(id=workshop.time_slot_id)
        location: Location = await Location.objects.aget(id=workshop.location_id)
        instructor: Instructor = await Instructor.objects.aget(id=workshop.instructor_id)
        start_datetime_with_tz = time_slot_obj.start_datetime.astimezone(tz=ZoneInfo(time_slot_obj.time_zone))
        end_datetime_with_tz = time_slot_obj.end_datetime.astimezone(tz=ZoneInfo(time_slot_obj.time_zone))
        return WorkshopDetail(
            id=workshop.id,
            title=workshop.title,
            description=workshop.description,
            location=LocationBase(
                id=location.id,
                name=location.name,
                address=location.address,
                floor=location.floor,
                room_number=location.room_number
            ),
            start_datetime=start_datetime_with_tz,
            end_datetime=end_datetime_with_tz,
            instructor=InstructorBase(
                id=instructor.id,
                name=instructor.name,
                bio=instructor.bio
            ),
            participants_limit=workshop.participants_limit,
            is_full=workshop.participants_limit <= await self.get_workshop_participants_count(workshop_id=workshop_id)
        )

    async def check_has_registered_at_timeslot(self, workshop: Workshop) -> bool:
        """
        Check has registered at timeslot

        :param workshop:
        :return:
        """
        account: Account = self._api_context.account
        filter_workshops = Workshop.objects.filter(
            time_slot=workshop.time_slot,
            is_removed=False
        ).all()
        async for filter_workshop in filter_workshops:
            workshop_registration = await WorkshopRegistration.objects.filter(
                workshop=filter_workshop,
                account=account,
                is_removed=False
            ).afirst()
            if workshop_registration:
                return True

    async def register_workshop(self, workshop_id: uuid.UUID) -> None:
        """
        Register workshop

        :param workshop_id:
        :return:
        """
        workshop: Workshop = await Workshop.objects.aget(id=workshop_id)
        if await self.check_has_registered_at_timeslot(workshop=workshop):
            raise APIException(
                status_code=400,
                message="You have already registered for a workshop at this time slot."
            )
        workshop_registration: WorkshopRegistration = WorkshopRegistration(
            workshop=workshop,
            account=self._api_context.account
        )
        await workshop_registration.asave()

    async def unregister_workshop(self, workshop_id: uuid.UUID) -> None:
        """
        Unregister workshop

        :param workshop_id:
        :return:
        """
        workshop: Workshop = await Workshop.objects.aget(id=workshop_id)
        workshop_registration: WorkshopRegistration = await WorkshopRegistration.objects.filter(
            workshop=workshop,
            account=self._api_context.account,
            is_removed=False
        ).afirst()
        if not workshop_registration:
            raise APIException(
                status_code=400,
                message="You have not registered for this workshop."
            )
        workshop_registration.is_removed = True
        workshop_registration.unregistered_at = datetime.now(tz=ZoneInfo("UTC"))
        await workshop_registration.asave()

    async def get_registered_workshops(self) -> dict[str, bool]:
        """
        Get registered workshops

        :return:
        """
        account: Account = self._api_context.account
        workshop_registrations = WorkshopRegistration.objects.filter(
            account=account,
            is_removed=False
        ).all()
        registered_workshops = {}
        async for workshop_registration in workshop_registrations:
            registered_workshops[workshop_registration.workshop_id.hex] = True if not workshop_registration.unregistered_at else False
        return registered_workshops

    @staticmethod
    async def get_workshop_participants_count(workshop_id) -> int:
        """
        Get workshop participants count

        :param workshop_id:
        :return:
        """
        return await WorkshopRegistration.objects.filter(
            workshop_id=workshop_id,
            is_removed=False
        ).acount()

