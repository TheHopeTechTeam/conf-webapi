"""
Test workshop handler
"""
import uuid

import pytest

from portal.handlers import WorkshopHandler


@pytest.mark.asyncio
async def test_unregister_workshop(
    workshop_handler: WorkshopHandler,
) -> None:
    """
    Test unregister workshop
    :param workshop_handler:
    :return:
    """
    workshop_id = uuid.UUID("89a95941-c91a-4222-9981-d871c7acaee3")
    result = await workshop_handler.unregister_workshop(
        workshop_id=workshop_id
    )
    assert result is None
