from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from core.pagination import ExtendedLimitOffsetPagination

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
    pagination_class = ExtendedLimitOffsetPagination

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
    serializer_class = OfferUpdateStatusSerializer
    lookup_field = "id"

    def get_queryset(self) -> QuerySet:
        return self.offer_service.all(is_active=True)


class OfferAgreementAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    offer_service = OfferService()
    permission_classes = [DjangoModelPermissions]
    serializer_class = OfferAgreementUpdateSerializer
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet["Offer"]:
        return self.offer_service.all(is_active=True, company_agreed=False)

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        self.offer_service.accept_offer_agreement(instance, request=request)
        response_data = {"detail": "accepted the offer"}
        return Response(response_data)
