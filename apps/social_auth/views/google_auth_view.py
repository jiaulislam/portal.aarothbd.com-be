from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.authentication.services import TokenService
from apps.user.services.user_service import UserService
from core.exceptions.common import CustomException
from core.request import Request

from ..serializers import GoogleAuthLoginSerializer
from ..services.google_auth_service import GoogleAuthProviderService

__all__ = ["GoogleSignInAuthAPIView"]


class GoogleSignInAuthAPIView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = GoogleAuthLoginSerializer
    google_auth_service = GoogleAuthProviderService()
    user_service = UserService()

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        user_data = self.google_auth_service.validate_token(serializer.validated_data.get("id_token"))
        if not self.google_auth_service.validate_user_data(user_data):
            exc = CustomException(detail="Unable to validate the user data.")
            exc.status_code = status.HTTP_400_BAD_REQUEST
            raise exc
        user_serializer_data = {
            "email": user_data.get("email"),
            "first_name": user_data.get("name"),
            "auth_provider": self.google_auth_service.provider,
        }
        user, _ = self.user_service.get_or_create_social_auth_user(user_serializer_data)  # type: ignore
        token_service = TokenService(request=request, user=user)
        response = token_service.get_secured_cookie_response()
        response.data = {"detail": "Logged in Successfully."}
        response.status_code = status.HTTP_200_OK
        return response
