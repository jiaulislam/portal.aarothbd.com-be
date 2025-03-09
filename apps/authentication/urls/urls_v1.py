from django.urls import path

from ..views import (
    LoginAPIView,
    LogoutAPIView,
    RefreshTokenAPIView,
    RegisterUserAPIView,
    ResetPasswordAPIView,
    ResetPasswordConfirmationAPIView,
)

urlpatterns = [
    path(r"register/", RegisterUserAPIView.as_view(), name="user-register"),
    path(r"login/", LoginAPIView.as_view(), name="user-login"),
    path(r"logout/", LogoutAPIView.as_view(), name="user-logout"),
    path(r"refresh-token/", RefreshTokenAPIView.as_view(), name="refresh-token"),
    path(r"reset-password/", ResetPasswordAPIView.as_view(), name="reset-password-view"),
    path(r"confirm-reset-password/", ResetPasswordConfirmationAPIView.as_view(), name="confirm-reset-password-view"),
]
