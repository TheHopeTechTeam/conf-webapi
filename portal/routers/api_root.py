"""
Root router.
"""
from django.conf import settings
from fastapi import APIRouter

from portal.apps.ticket.router import router as ticket_router
from portal.libs.depends import DEFAULT_RATE_LIMITERS
from .apis.v1 import router as api_v1_router

if settings.REDIS_URL:
    router = APIRouter(
        dependencies=[
            *DEFAULT_RATE_LIMITERS
        ],
    )
else:
    router = APIRouter()
router.include_router(api_v1_router, prefix="/v1")
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
