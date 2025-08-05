from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filter import PurchaseOrderFilter
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer


class PurchaseOrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all().select_related("supplier").prefetch_related("order_lines")
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase_order = serializer.save()
        response = PurchaseOrderSerializer(purchase_order).data
        return Response(response, status=status.HTTP_201_CREATED)
