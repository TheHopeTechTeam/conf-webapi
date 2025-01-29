"""
FeedbackHandler
"""
from portal.apps.feedback.models import Feedback
from portal.serializers.v1.feedback import FeedbackCreate, FeedbackCreateResponse


class FeedbackHandler:
    """FeedbackHandler"""

    def __init__(self):
        pass

    async def creat_feedback(self, model: FeedbackCreate) -> FeedbackCreateResponse:
        """
        Create feedback
        """
        data = model.model_dump()
        feedback_obj = await Feedback.objects.acreate(**data)
        return FeedbackCreateResponse(id=feedback_obj.id)
