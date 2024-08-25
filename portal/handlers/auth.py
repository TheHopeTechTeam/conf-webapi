"""
Handler for authentication
"""
from portal.providers.firebase.base import FirebaseProvider
from portal.schemas.auth import FirebaseTokenPayload


class AuthHandler:
    """AuthHandler"""

    def __init__(
        self,
    ):
        self.firebase_provider: FirebaseProvider = FirebaseProvider()

    async def verify_firebase_token(
        self,
        token: str
    ) -> FirebaseTokenPayload:
        """

        :param token:
        :return:
        """
        user_info = self.firebase_provider.authentication.verify_id_token(id_token=token)
        return FirebaseTokenPayload(**user_info)
