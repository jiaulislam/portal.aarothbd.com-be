from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filter import PurchaseOrderFilter
from .models import PurchaseOrder
from .serializers import PurchaseOrderLineSerializer, PurchaseOrderRetrieveSerializer, PurchaseOrderSerializer


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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_lines_data = serializer.validated_data.pop("order_lines", [])
        purchase_order = serializer.save()

        # Bulk create order lines
        if order_lines_data:
            from .models import PurchaseOrderLine  # Assuming this model exists

            order_lines = [
                PurchaseOrderLine(purchase_order=purchase_order, **line_data) for line_data in order_lines_data
            ]
            PurchaseOrderLine.objects.bulk_create(order_lines)
        # Update stock quantities after creating the purchase order
        purchase_order.update_stock_quantity()
        response = PurchaseOrderSerializer(purchase_order).data
        return Response(response, status=status.HTTP_201_CREATED)


class PurchaseOrderRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderRetrieveSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all().select_related("supplier").prefetch_related("order_lines")
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseOrderLineCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderLineSerializer
    lookup_field = "id"
    queryset = PurchaseOrder.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase_order = self.queryset.get(id=self.kwargs["id"])
        purchase_order_line = serializer.save(purchase_order=purchase_order)
        # Update stock quantities after creating the purchase order
        purchase_order.update_stock_quantity()
        response = PurchaseOrderLineSerializer(purchase_order_line).data
        return Response(response, status=status.HTTP_201_CREATED)
