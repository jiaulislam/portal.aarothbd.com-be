from django.urls import path

from .views import ActionListAPIView

urlpatterns = [
    path(r"actions/", ActionListAPIView.as_view(), name="action-list"),
]
