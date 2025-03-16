from django.urls import path

from .views import AboutUsAPIView

urlpatterns = [
    path(r"about-us/", AboutUsAPIView.as_view(), name="about-us-view"),
]
