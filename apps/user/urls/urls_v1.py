from django.urls import path

from ..views.views_v1 import (
    CookieTokenRefreshView,
    LoginAPIView,
    LogoutView,
    MeAPIView,
    RegisterUserAPIView,
)

urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="auth-register"),
    path("login/", LoginAPIView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeAPIView.as_view(), name="auth-me"),
    path(
        "refresh-token/",
        CookieTokenRefreshView.as_view(),
        name="auth-refresh-token",
    ),
]
