from django.urls import path

from ..views.company_address_view_v1 import CompanyAddressCreateAPIView
from ..views.company_view_v1 import (
    CompanyListCreateAPIView,
    CompanyRetrieveUpdateAPIView,
    CompanyUpdateStatusAPIView,
)

urlpatterns = [
    path(r"companies/", CompanyListCreateAPIView.as_view(), name="companies-list-create"),
    path(r"companies/<int:id>/", CompanyRetrieveUpdateAPIView.as_view(), name="company-retrieve-update"),
    path(r"companies/<int:id>/update-status/", CompanyUpdateStatusAPIView.as_view(), name="company-update-status"),
    path(r"companies/<int:company_id>/address/", CompanyAddressCreateAPIView.as_view(), name="company-address-create"),
]
