"""
WorkshopHandler
"""
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.cache import BaseCache, cache

from portal.apps.account.models import Account
from portal.apps.location.models import Location
from portal.apps.workshop.models import Workshop, WorkshopRegistration
from portal.exceptions.api_base import APIException
from portal.libs.contexts.api_context import APIContext, get_api_context
from portal.serializers.v1.workshop import WorkshopList, WorkshopBase


class WorkshopHandler:
    """WorkshopHandler"""

    def __init__(self):
        try:
            self._api_context: APIContext = get_api_context()
        except Exception:
            self._api_context = None
        self._cache: BaseCache = cache

    async def get_workshop_list(self) -> WorkshopList:
        """
        Get the workshop list

        :return:
        """
        # TODO: Implement the cache mechanism
        workshop_iterator = Workshop.objects.filter(is_removed=False).all()
        workshops = []
        async for workshop in workshop_iterator:
            start_datetime = workshop.start_datetime.astimezone(ZoneInfo(workshop.time_zone))
            end_datetime = workshop.end_datetime.astimezone(ZoneInfo(workshop.time_zone))
            location = await Location.objects.filter(id=workshop.location_id).afirst()
            workshops.append(
                WorkshopBase(
                    id=workshop.id,
                    title=workshop.title,
                    description=workshop.description,
                    location=location.name,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime
                )
            )
        return WorkshopList(workshops=workshops)

    async def check_has_registered_at_timeslot(self, workshop: Workshop) -> bool:
        """
        Check has registered at timeslot

        :param workshop:
        :return:
        """
        account: Account = self._api_context.account
        filter_workshops = Workshop.objects.filter(
            start_datetime__gte=workshop.start_datetime,
            end_datetime__lte=workshop.end_datetime,
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
