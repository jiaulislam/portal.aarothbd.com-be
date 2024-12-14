from django.urls import path

from ..views.company_address_view_v1 import CompanyAddressListCreateAPIView
from ..views.company_configuration_view_v1 import CompanyConfigurationUpdateAPIView
from ..views.company_view_v1 import (
    CompanyListCreateAPIView,
    CompanyRetrieveUpdateAPIView,
    CompanyUpdateStatusAPIView,
)

urlpatterns = [
    path(r"companies/", CompanyListCreateAPIView.as_view(), name="companies-list-create"),
    path(r"companies/<int:id>/", CompanyRetrieveUpdateAPIView.as_view(), name="company-retrieve-update"),
    path(
        r"companies/<int:id>/update-status/",
        CompanyUpdateStatusAPIView.as_view(),
        name="company-update-status",
    ),
    path(
        r"companies/<int:company_id>/addresses/",
        CompanyAddressListCreateAPIView.as_view(),
        name="company-addresses-list-create",
    ),
    path(
        r"companies/<int:company_id>/configuration/",
        CompanyConfigurationUpdateAPIView.as_view(),
        name="company-configuration-update",
    ),
]
