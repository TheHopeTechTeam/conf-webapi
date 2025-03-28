"""
Test account handler
"""
import uuid

import pytest

from portal.handlers import AccountHandler


@pytest.mark.asyncio
async def test_get_account(account_handler: AccountHandler, account_id: uuid.UUID):
    """
    Test get account
    :param account_handler:
    :param account_id:
    :return:
    """
    result = await account_handler.get_account(account_id=account_id)
    assert result.id == account_id
