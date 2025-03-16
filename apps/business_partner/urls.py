from django.urls import path

from .views import BusinessPartnerListAPIView

urlpatterns = [
    path(r"business-partners/", BusinessPartnerListAPIView.as_view(), name="business-partners-list-view"),
]
