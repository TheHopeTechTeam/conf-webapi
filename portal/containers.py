"""
Container
"""
from dependency_injector import containers, providers

from portal.handlers import (
    UserHandler,
)
from portal.libs.database import RedisPool


# pylint: disable=too-few-public-methods,c-extension-no-member
class Container(containers.DeclarativeContainer):
    """Container"""

    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=["portal.handlers", "portal.routers"],
    )

    # [database]
    redis_pool = providers.Singleton(RedisPool)

    # [handlers]
    user_handler = providers.Factory(
        UserHandler,
        # redis=redis_pool
    )
