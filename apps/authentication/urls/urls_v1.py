from django.urls import path

from ..views import LoginAPIView, RegisterUserAPIView

urlpatterns = [
    path(r"register/", RegisterUserAPIView.as_view(), name="user-register"),
    path(r"login/", LoginAPIView.as_view(), name="user-login"),
]
