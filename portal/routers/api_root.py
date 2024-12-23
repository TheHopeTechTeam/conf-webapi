"""
Root router.
"""
from fastapi import APIRouter

from portal.apps.ticket.router import router as ticket_router
from .apis.v1 import router as api_v1_router

router = APIRouter()
router.include_router(api_v1_router, prefix="/v1", tags=["API v1"])
router.include_router(ticket_router, prefix="/ticket", tags=["Ticket"])


@router.get(
    path="/healthz"
)
async def healthz():
    """
    Healthcheck endpoint
    :return:
    """
    return {
        "message": "ok"
    }
