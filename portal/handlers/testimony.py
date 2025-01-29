"""
TestimonyHandler
"""
from portal.apps.testimony.models import Testimony
from portal.serializers.v1.testimony import TestimonyCreate, TestimonyCreateResponse


class TestimonyHandler:
    """TestimonyHandler"""

    def __init__(self):
        pass

    async def create_testimony(self, model: TestimonyCreate) -> TestimonyCreateResponse:
        """
        Create testimony
        """
        data = model.model_dump(exclude_none=True)
        testimony_obj = await Testimony.objects.acreate(**data)
        return TestimonyCreateResponse(id=testimony_obj.id)

