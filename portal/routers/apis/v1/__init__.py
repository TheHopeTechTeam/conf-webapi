"""
Top level router for v1 API
"""
from fastapi import APIRouter
from .account import router as account_router
from .workshop import router as workshop_router

router = APIRouter()
router.include_router(account_router, prefix="/account", tags=["Account"])
router.include_router(workshop_router, prefix="/workshop", tags=["Workshop"])

