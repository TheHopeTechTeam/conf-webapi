"""
FirebaseAuthentication
"""
from firebase_admin import auth
from firebase_admin.auth import UserRecord


class FirebaseAuthentication:
    """FirebaseAuthentication"""

    def __init__(self, app: str = None):
        """initialize"""
        self.app = app

    def verify_id_token(
        self,
        id_token: str,
        check_revoked: bool = False,
        clock_skew_seconds: int = 0
    ) -> dict:
        """
        Verify id token
        :param id_token:
        :param check_revoked:
        :param clock_skew_seconds:
        :return:
        """
        return auth.verify_id_token(
            id_token=id_token,
            app=self.app,
            check_revoked=check_revoked,
            clock_skew_seconds=clock_skew_seconds
        )

    def get_user(self, uid: str) -> UserRecord:
        """
        Get user
        """
        return auth.get_user(uid=uid, app=self.app)
