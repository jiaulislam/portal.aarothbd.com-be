from django.urls import path

from .views import ContactUsCreateAPIView

urlpatterns = [
    path(r"contact-us/", ContactUsCreateAPIView.as_view(), name="contact-us-view"),
]
