from django.urls import path

from .views import ActionExecuteAPIView, ActionListAPIView

urlpatterns = [
    path(r"actions/", ActionListAPIView.as_view(), name="action-list"),
    path(r"actions/execute/", ActionExecuteAPIView.as_view(), name="action-execute"),
]
