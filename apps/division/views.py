from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from .filters import DivisionFilter
from .serializers import DivisionSerializer
from .services import DivisionService


class DivisionListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DivisionSerializer
    filterset_class = DivisionFilter
    pagination_class = ExtendedLimitOffsetPagination
    service_class = DivisionService()

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
