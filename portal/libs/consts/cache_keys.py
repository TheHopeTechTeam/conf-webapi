"""
Constants for Cache keys
"""
from django.conf import settings


def get_cache_key(key: str) -> str:
    """
    Get Cache key
    :param key:
    :return:
    """
    return f"{settings.APP_NAME}:{key}"


def get_firebase_signed_url_key(image_id: int) -> str:
    """
    Get the Firebase signed URL key
    :param image_id:
    :return:
    """
    return get_cache_key(f"firebase:signed_url:{image_id}")
