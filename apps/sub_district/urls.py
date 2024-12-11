from django.urls import path

from .views import SubDistrictListAPIView

urlpatterns = [
    path(r"sub-districts/", SubDistrictListAPIView.as_view(), name="sub-district-list"),
]
