from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from .filters import CountryFilter
from .serializers import CountrySerializer
from .services import CountryService


class CountryListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CountrySerializer
    filterset_class = CountryFilter
    pagination_class = ExtendedLimitOffsetPagination

    service_class = CountryService()

    def get_queryset(self):
        queryset = self.service_class.all()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        page = self.pagination_class()
        paginated_queryset = page.paginate_queryset(queryset, request)
        serialized = self.serializer_class(instance=paginated_queryset, many=True)
        return page.get_paginated_response(serialized.data)
