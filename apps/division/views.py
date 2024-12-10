from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from .filters import DivisionFilter
from .models import Division
from .serializers import DivisionSerializer


class DivisionListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DivisionSerializer
    filterset_class = DivisionFilter
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self):
        queryset = Division.objects.all()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        page = self.pagination_class()
        paginated_queryset = page.paginate_queryset(queryset, request)
        serialized = self.serializer_class(instance=paginated_queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
