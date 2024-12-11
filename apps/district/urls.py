from django.urls import path

from .views import DistrictListAPIView

urlpatterns = [
    path(r"districts/", DistrictListAPIView.as_view(), name="districts-list"),
]
