from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from .filters import CountryFilter
from .models import Country
from .serializers import CountrySerializer


class CountryListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CountrySerializer
    filterset_class = CountryFilter
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self):
        queryset = Country.objects.all()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        page = self.pagination_class()
        paginated_queryset = page.paginate_queryset(queryset, request)
        serialized = self.serializer_class(instance=paginated_queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
