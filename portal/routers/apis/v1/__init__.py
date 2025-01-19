"""
Top level router for v1 API
"""
from fastapi import APIRouter
from .account import router as account_router
from .faq import router as faq_router
from .workshop import router as workshop_router

router = APIRouter()
router.include_router(account_router, prefix="/account", tags=["Account"])
router.include_router(faq_router, prefix="/faq", tags=["FAQ"])
router.include_router(workshop_router, prefix="/workshop", tags=["Workshop"])

