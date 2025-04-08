from django.urls import path

from .views.cupon_view_v1 import CuponValidateAPIView
from .views.offer_views_v1 import (
    EcommerceOfferListAPIView,
    OfferAgreementAPIView,
    OfferListCreateAPIView,
    OfferRetrieveUpdateAPIView,
    OfferUpdateStatusAPIView,
)

urlpatterns = [
    path(r"offers/", OfferListCreateAPIView.as_view(), name="offer-list-create-view"),
    path(r"ecomm/offers/", EcommerceOfferListAPIView.as_view(), name="ecomm-offer-list-create-view"),
    path(r"offers/<str:slug>/", OfferRetrieveUpdateAPIView.as_view(), name="offer-retrieve-update-view"),
    path(r"offers/<str:id>/update-status/", OfferUpdateStatusAPIView.as_view(), name="offer-update-status-view"),
    path(r"offers/<str:slug>/update-agreement/", OfferAgreementAPIView.as_view(), name="offer-update-agreement-view"),
    path(r"cupons/<str:cupon_code>/validate/", CuponValidateAPIView.as_view(), name="cupon-validate-view"),
]
