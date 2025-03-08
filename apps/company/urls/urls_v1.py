from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views.company_address_view_v1 import CompanyAddressListCreateAPIView
from ..views.company_configuration_view_v1 import CompanyConfigurationUpdateAPIView
from ..views.company_view_v1 import (
    CompanyCategoryViewSet,
    CompanyImageUploadAPIView,
    CompanyListCreateAPIView,
    CompanyRetrieveUpdateAPIView,
    CompanyUpdateStatusAPIView,
)

router = DefaultRouter()

router.register(r"company-categories", CompanyCategoryViewSet, basename="company-categories")


urlpatterns = [
    path(r"companies/", CompanyListCreateAPIView.as_view(), name="companies-list-create"),
    path(r"companies/<int:id>/", CompanyRetrieveUpdateAPIView.as_view(), name="company-retrieve-update"),
    path(
        r"companies/<int:id>/update-status/",
        CompanyUpdateStatusAPIView.as_view(),
        name="company-update-status",
    ),
    path(
        r"companies/<int:id>/upload-image/",
        CompanyImageUploadAPIView.as_view(),
        name="company-upload-image",
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
    path(r"", include(router.urls)),
]
