from django.urls import path

from ..views.views_v1 import (
    CookieTokenRefreshView,
    LoginView,
    LogoutView,
    MeView,
    RegisterAccountView,
)

urlpatterns = [
    path("register/", RegisterAccountView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me"),
    path(
        "refresh-token/",
        CookieTokenRefreshView.as_view(),
        name="auth-refresh-token",
    ),
]
