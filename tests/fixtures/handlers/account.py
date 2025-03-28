"""
Fixtures for account handler tests.
"""
import uuid

import pytest

from portal.apps.account.models import Account
from portal.containers import Container
from portal.handlers import AccountHandler
from portal.libs.contexts.api_context import set_api_context, APIContext

@pytest.fixture
def account_id() -> uuid.UUID:
    """Get the account."""
    return uuid.UUID("ca659ec3-5514-485a-a181-4491031b81b1")


@pytest.fixture
def account_handler(account_id: uuid.UUID) -> AccountHandler:
    """Get the file handler."""
    set_api_context(
        APIContext(
            account=Account.objects.get(id=account_id)
        )
    )
    return Container.account_handler()
