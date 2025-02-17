from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.serializers import BaseSerializer

if TYPE_CHECKING:
    from apps.offer.models import Offer


from ..filters import OfferFilter
from ..serializers import (
    OfferAgreementUpdateSerializer,
    OfferCreateUpdateSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferUpdateStatusSerializer,
)
from ..services import OfferService


class OfferListCreateAPIView(ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    offer_service = OfferService()
    filterset_class = OfferFilter

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return OfferListSerializer
        return OfferCreateUpdateSerializer

    def get_queryset(self) -> QuerySet["Offer"]:
        queryset = self.offer_service.all()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs


class OfferRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "post"]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    offer_service = OfferService()
    lookup_field = "slug"

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return OfferRetrieveSerializer
        return OfferCreateUpdateSerializer

    def get_queryset(self) -> QuerySet["Offer"]:
        return self.offer_service.all()


class OfferUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    permission_classes = [DjangoModelPermissions]
    offer_service = OfferService()
    lookup_field = "slug"
    serializer_class = OfferUpdateStatusSerializer


class OfferAgreementAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    offer_service = OfferService()
    serializer_class = OfferAgreementUpdateSerializer
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet["Offer"]:
        return self.offer_service.all(is_active=True, company_agreed=False)
