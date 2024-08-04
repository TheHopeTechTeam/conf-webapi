"""
Container
"""
from dependency_injector import containers, providers

from app.config import settings
from app.handlers import (
    UserHandler,
)
from app.libs.database import RedisPool, Session


# pylint: disable=too-few-public-methods,c-extension-no-member
class Container(containers.DeclarativeContainer):
    """Container"""

    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=["app.handlers", "app.routers"],
    )

    # [database]
    aio_session = providers.Singleton(Session)
    redis_pool = providers.Singleton(RedisPool)

    # [handlers]
    user_handler = providers.Factory(
        UserHandler,
        # redis=redis_pool
    )
