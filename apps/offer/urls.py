from django.urls import path

from .views.offer_views_v1 import (
    OfferAgreementAPIView,
    OfferListCreateAPIView,
    OfferRetrieveUpdateAPIView,
    OfferUpdateStatusAPIView,
)

urlpatterns = [
    path(r"offers/", OfferListCreateAPIView.as_view(), name="offer-list-create-view"),
    path(r"offers/<str:slug>/", OfferRetrieveUpdateAPIView.as_view(), name="offer-retrieve-update-view"),
    path(r"offers/<str:slug>/update-status/", OfferUpdateStatusAPIView.as_view(), name="offer-update-status-view"),
    path(r"offers/<str:slug>/update-agreement/", OfferAgreementAPIView.as_view(), name="offer-update-agreement-view"),
]
