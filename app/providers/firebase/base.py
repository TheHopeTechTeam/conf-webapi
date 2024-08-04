"""
FirebaseProvider
"""
from .authentication import FirebaseAuthentication


class FirebaseProvider:
    """FirebaseProvider"""

    def __init__(self, app: str = "default"):
        """initialize"""
        self.app = app

    @property
    def authentication(self) -> FirebaseAuthentication:
        """
        authentication
        """
        return FirebaseAuthentication(app=self.app)
