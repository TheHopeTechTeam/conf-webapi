"""
FirebaseProvider
"""
from firebase_admin import App

from .authentication import FirebaseAuthentication


class FirebaseProvider:
    """FirebaseProvider"""

    def __init__(self, app: App = None):
        """initialize"""
        self.app = app

    @property
    def authentication(self) -> FirebaseAuthentication:
        """
        authentication
        """
        return FirebaseAuthentication(app=self.app)
