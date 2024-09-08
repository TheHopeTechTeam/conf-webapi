"""
Util functions for lifespan
"""
from contextlib import asynccontextmanager

from django.conf import settings
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from portal.libs.database import RedisPool
from portal.libs.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan
    :param _:
    """
    logger.info("Starting lifespan")
    redis_connection = RedisPool().create(db=1)
    await FastAPILimiter.init(
        redis=redis_connection,
        prefix=f"{settings.APP_NAME}_limiter"
    )
    yield
    await FastAPILimiter.close()
