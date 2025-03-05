"""
ConferenceHandler
"""
import uuid

from portal.apps.conference.models import Conference
from portal.apps.location.models import Location
from portal.handlers import FileHandler
from portal.libs.consts.enums import Rendition
from portal.serializers.v1.conference import ConferenceBase, ConferenceDetail, ConferenceList
from portal.serializers.v1.instructor import InstructorBase
from portal.serializers.v1.location import LocationBase


class ConferenceHandler:
    """ConferenceHandler"""

    def __init__(
        self,
        file_handler: FileHandler,
    ):
        self._file_handler = file_handler

    async def get_conferences(self) -> ConferenceList:
        """
        Get conference
        :return:
        """
        conference_list = []
        objs = Conference.objects.filter(is_removed=False).all()
        async for obj in objs:
            conference_list.append(
                ConferenceBase(
                    id=obj.id,
                    title=obj.title,
                    start_date=obj.start_date,
                    end_date=obj.end_date
                )
            )
        return ConferenceList(conferences=conference_list)

    async def get_active_conference(self) -> ConferenceDetail:
        """
        Get an active conference
        :return:
        """
        obj: Conference = await Conference.objects.filter(is_removed=False, active=True).afirst()  # noqa
        active_obj = await self.get_conference_detail(conference_id=obj.id)
        return active_obj


    async def get_conference_detail(self, conference_id: uuid.UUID) -> ConferenceDetail:
        """
        Get conference detail
        :param conference_id:
        :return:
        """
        obj: Conference = await Conference.objects.aget(id=conference_id)  # noqa
        location_obj: Location = await Location.objects.aget(id=obj.location_id)
        instructor_list = []
        instructor_objs = obj.instructors.order_by("sort_order").all()
        async for instructor in instructor_objs:
            instructor_list.append(
                InstructorBase(
                    id=instructor.id,
                    name=instructor.name,
                    title=instructor.title,
                    bio=instructor.bio,
                    image_url=await self._file_handler.get_file_url(
                        image_id=instructor.image_id,
                        rendition=Rendition.MAX_100x100.value
                    )
                )
            )

        return ConferenceDetail(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            start_date=obj.start_date,
            end_date=obj.end_date,
            location=LocationBase(
                id=location_obj.id,
                name=location_obj.name,
                address=location_obj.address,
                floor=location_obj.floor
            ),
            instructors=instructor_list
        )
