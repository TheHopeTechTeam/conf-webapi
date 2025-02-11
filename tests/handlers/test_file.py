"""
Test file handler
"""
import pytest

from portal.handlers import FileHandler


@pytest.mark.asyncio
async def test_get_file_url(file_handler: FileHandler):
    """
    Test get file url
    :param file_handler:
    :return:
    """
    image_id: int = 7
    result = await file_handler.get_file_url(image_id=image_id)
    print(result)
