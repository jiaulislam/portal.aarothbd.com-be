from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

from apps.user.constants import AuthProviderChoices
from core.exceptions.common import CustomException

from .base_auth_service import BaseSocialAuthProviderService

__all__ = ["GoogleAuthProviderService"]


class GoogleAuthProviderService(BaseSocialAuthProviderService):
    provider = AuthProviderChoices.GOOGLE

    def __init__(self):
        pass

    def validate_token(self, auth_token: str):
        """validate the given oauth2 token from the oauth2 provider"""
        try:
            user_info = id_token.verify_oauth2_token(auth_token, requests.Request())
            if self.provider not in user_info["iss"]:
                raise ValueError("Invalid provider while validating Google Provider.")

            return user_info
        except (ValueError, GoogleAuthError) as exc:
            raise CustomException(detail=str(exc), code="client_error")

    def validate_user_data(self, user_data):
        return True
