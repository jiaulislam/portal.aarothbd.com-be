from django.urls import path

from .views import AddressRetrieveUpdateDestroyAPIView

urlpatterns = [
    path(r"addresses/<int:id>/", AddressRetrieveUpdateDestroyAPIView.as_view(), name="address-update-retrieve-destroy"),
]
