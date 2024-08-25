"""
Util functions for lifespan
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from portal.config import configs
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
        prefix=f"{configs.APP_NAME}_limiter"
    )
    yield
    await FastAPILimiter.close()
