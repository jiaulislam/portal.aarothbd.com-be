from django.urls import path

from ..views import LoginAPIView, LogoutAPIView, RefreshTokenAPIView, RegisterUserAPIView

urlpatterns = [
    path(r"register/", RegisterUserAPIView.as_view(), name="user-register"),
    path(r"login/", LoginAPIView.as_view(), name="user-login"),
    path(r"logout/", LogoutAPIView.as_view(), name="user-logout"),
    path(r"refresh-token/", RefreshTokenAPIView.as_view(), name="refresh-token"),
]
