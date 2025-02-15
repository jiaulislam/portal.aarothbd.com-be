from django.urls import path

from .views import GoogleSignInAuthAPIView

urlpatterns = [
    path(r"oauth2/google/login/", GoogleSignInAuthAPIView.as_view(), name="google-social-auth"),
]
