"""
WorkshopHandler
"""
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.cache import BaseCache, cache
from django.db import IntegrityError

from portal.apps.account.models import Account
from portal.apps.instructor.models import Instructor
from portal.apps.location.models import Location
from portal.apps.workshop.models import WorkshopTimeSlot, Workshop, WorkshopRegistration
from portal.exceptions.api_base import APIException
from portal.handlers import FileHandler
from portal.libs.consts.enums import Rendition
from portal.libs.contexts.api_context import APIContext, get_api_context
from portal.serializers.v1.instructor import InstructorBase
from portal.serializers.v1.location import LocationBase
from portal.serializers.v1.workshop import (
    WorkshopBase,
    WorkshopDetail,
    WorkshopSchedule,
    WorkshopScheduleList,
    WorkshopRegistered,
    WorkshopRegisteredList,
)


class WorkshopHandler:
    """WorkshopHandler"""

    def __init__(
        self,
        file_handler: FileHandler,
    ):
        self._file_handler = file_handler
        try:
            self._api_context: APIContext = get_api_context()
        except Exception:
            self._api_context = None
        self._cache: BaseCache = cache

    async def get_workshop_schedule_list(self) -> WorkshopScheduleList:
        """
        Get the workshop list

        :return:
        """
        workshop_schedules = []
        workshop_time_slots = WorkshopTimeSlot.objects.filter(is_removed=False).order_by("start_datetime").all()
        async for workshop_time_slot in workshop_time_slots:
            workshops = Workshop.objects.filter(
                time_slot=workshop_time_slot,
                is_removed=False
            ).all()
            workshop_list = []
            async for workshop in workshops:
                location: Location = await Location.objects.aget(id=workshop.location_id)
                workshop_list.append(
                    WorkshopBase(
                        id=workshop.id,
                        title=workshop.title,
                        description=workshop.description,
                        location=LocationBase(
                            id=location.id,
                            name=location.name,
                            address=location.address,
                            floor=location.floor,
                            room_number=location.room_number,
                            image_url=await self._file_handler.get_file_url(
                                image_id=location.image_id,
                                rendition=Rendition.MAX_800x800.value
                            )
                        ),
                        slido_url=workshop.slido_url
                    )
                )
            workshop_schedules.append(
                WorkshopSchedule(
                    start_datetime=workshop_time_slot.start_datetime.astimezone(tz=ZoneInfo(workshop_time_slot.time_zone)),
                    end_datetime=workshop_time_slot.end_datetime.astimezone(tz=ZoneInfo(workshop_time_slot.time_zone)),
                    workshops=workshop_list
                )
            )

        return WorkshopScheduleList(schedule=workshop_schedules)

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
                room_number=location.room_number,
                image_url=await self._file_handler.get_file_url(
                    image_id=location.image_id,
                    rendition=Rendition.MAX_800x800.value
                )
            ),
            start_datetime=start_datetime_with_tz,
            end_datetime=end_datetime_with_tz,
            instructor=InstructorBase(
                id=instructor.id,
                name=instructor.name,
                title=instructor.title,
                bio=instructor.bio,
                image_url=await self._file_handler.get_file_url(
                    image_id=instructor.image_id,
                    rendition=Rendition.MAX_100x100.value
                )
            ),
            participants_limit=workshop.participants_limit,
            is_full=workshop.participants_limit <= await self.get_workshop_participants_count(workshop_id=workshop_id),
            image_url=await self._file_handler.get_file_url(
                image_id=workshop.image_id,
                rendition=Rendition.MAX_500x500.value
            ),
            slido_url=workshop.slido_url
        )

    async def check_has_registered_at_timeslot(self, workshop: Workshop) -> bool:
        """
        Check has registered at timeslot

        :param workshop:
        :return:
        """
        account: Account = self._api_context.account
        time_slot_obj: WorkshopTimeSlot = await WorkshopTimeSlot.objects.aget(id=workshop.time_slot_id)
        filter_workshops = Workshop.objects.filter(
            time_slot=time_slot_obj,
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
        if workshop.participants_limit <= await self.get_workshop_participants_count(workshop_id=workshop_id):
            raise APIException(
                status_code=400,
                message="The workshop is full."
            )
        # Check if the user has already registered for the workshop and unregistered
        # If so, update the registration
        workshop_registration: WorkshopRegistration = await WorkshopRegistration.all_objects.filter(
            workshop=workshop,
            account=self._api_context.account,
        ).afirst()
        if workshop_registration:
            workshop_registration.is_removed = False
            workshop_registration.unregistered_at = None
            await workshop_registration.asave()
            return
        try:
            await WorkshopRegistration.objects.acreate(
                workshop=workshop,
                account=self._api_context.account
            )
        except IntegrityError:
            raise APIException(
                status_code=400,
                message="You have already registered for this workshop."
            )

    async def unregister_workshop(self, workshop_id: uuid.UUID) -> None:
        """
        Unregister workshop

        :param workshop_id:
        :return:
        """
        workshop: Workshop = await Workshop.objects.aget(id=workshop_id)
        workshop_registration: WorkshopRegistration = await WorkshopRegistration.all_objects.filter(
            workshop=workshop,
            account=self._api_context.account
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
            registered_workshops[str(workshop_registration.workshop_id)] = True if not workshop_registration.unregistered_at else False
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

    async def get_my_workshops(self) -> WorkshopRegisteredList:
        """
        Get my workshops

        :return:
        """
        account: Account = self._api_context.account
        workshop_registrations = (
            WorkshopRegistration.objects.filter(
                account=account,
                is_removed=False,
                unregistered_at=None
            )
            .order_by("workshop__time_slot__start_datetime")
            .all()
        )
        my_workshops = []
        async for workshop_registration in workshop_registrations:
            workshop: Workshop = await Workshop.objects.aget(id=workshop_registration.workshop_id)
            location: Location = await Location.objects.aget(id=workshop.location_id)
            time_slot_obj: WorkshopTimeSlot = await WorkshopTimeSlot.objects.aget(id=workshop.time_slot_id)
            start_datetime_with_tz = time_slot_obj.start_datetime.astimezone(tz=ZoneInfo(time_slot_obj.time_zone))
            end_datetime_with_tz = time_slot_obj.end_datetime.astimezone(tz=ZoneInfo(time_slot_obj.time_zone))
            my_workshops.append(
                WorkshopRegistered(
                    id=workshop.id,
                    title=workshop.title,
                    description=workshop.description,
                    location=LocationBase(
                        id=location.id,
                        name=location.name,
                        address=location.address,
                        floor=location.floor,
                        room_number=location.room_number,
                        image_url=await self._file_handler.get_file_url(
                            image_id=location.image_id,
                            rendition=Rendition.MAX_800x800.value
                        )
                    ),
                    start_datetime=start_datetime_with_tz,
                    end_datetime=end_datetime_with_tz,
                    is_registered=True,
                    slido_url=workshop.slido_url
                )
            )

        return WorkshopRegisteredList(workshops=my_workshops)
