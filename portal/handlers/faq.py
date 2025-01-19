"""
FAQ handler
"""
import uuid

from portal.apps.faq.models import FaqCategory, Faq

from portal.serializers.v1.faq import FaqCategoryBase, FaqCategoryList, FaqList, FaqBase


class FAQHandler:
    """FAQ handler"""

    def __init__(self):
        pass

    @staticmethod
    async def get_faq_categories() -> FaqCategoryList:
        """
        Get FAQ categories
        """
        categories = []
        category_objs = FaqCategory.objects.all().order_by("sort_order")
        async for category_obj in category_objs:
            category = FaqCategoryBase(
                id=category_obj.id,
                name=category_obj.name,
                description=category_obj.description
            )
            categories.append(category)
        return FaqCategoryList(categories=categories)

    @staticmethod
    async def get_category_by_id(category_id: uuid.UUID) -> FaqCategoryBase:
        """
        Get category by ID
        """
        category_obj: FaqCategory = await FaqCategory.objects.aget(id=category_id)
        return FaqCategoryBase(
            id=category_obj.id,
            name=category_obj.name,
            description=category_obj.description
        )


    @staticmethod
    async def get_faq_by_id(faq_id: uuid.UUID) -> FaqBase:
        """
        Get FAQ by ID
        """
        faq_obj: Faq = await Faq.objects.aget(id=faq_id)
        return FaqBase(
            id=faq_obj.id,
            category_id=faq_obj.category_id,
            question=faq_obj.question,
            answer=faq_obj.answer,
            related_link=faq_obj.related_link
        )

    @staticmethod
    async def get_faqs_by_category(category_id: uuid.UUID) -> FaqList:
        """
        Get FAQs by category
        """
        faqs = []
        faq_objs = Faq.objects.filter(category_id=category_id).order_by("sort_order")
        async for faq_obj in faq_objs:
            faq = FaqBase(
                id=faq_obj.id,
                category_id=category_id,
                question=faq_obj.question,
                answer=faq_obj.answer,
                related_link=faq_obj.related_link
            )
            faqs.append(faq)
        return FaqList(faqs=faqs)
