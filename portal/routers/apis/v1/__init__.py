"""
Top level router for v1 API
"""
from fastapi import APIRouter
from .account import router as account_router
from .conference import router as conference_router
from .event_info import router as event_info_router
from .faq import router as faq_router
from .workshop import router as workshop_router

router = APIRouter()
router.include_router(account_router, prefix="/account", tags=["Account"])
router.include_router(conference_router, prefix="/conference", tags=["Conference"])
router.include_router(event_info_router, prefix="/event_info", tags=["Event Info"])
router.include_router(faq_router, prefix="/faq", tags=["FAQ"])
router.include_router(workshop_router, prefix="/workshop", tags=["Workshop"])

