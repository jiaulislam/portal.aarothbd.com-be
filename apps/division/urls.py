from django.urls import path

from .views import DivisionListAPIView

urlpatterns = [
    path(r"divisions/", DivisionListAPIView.as_view(), name="division-list"),
]
