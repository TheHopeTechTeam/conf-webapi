"""
Container
"""
from dependency_injector import containers, providers

from portal.handlers import (
    AccountHandler,
    WorkshopHandler,
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
    account_handler = providers.Factory(
        AccountHandler,
        # redis=redis_pool
    )
    workshop_handler = providers.Factory(
        WorkshopHandler,
        # redis=redis_pool
    )
