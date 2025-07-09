import random
import string
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..constants import OrderStatusChoice
from ..models import OrderDelivery, OrderDeliveryBill, OrderDeliveryLine
from ..serializers import (
    OrderDeliveryBillSerializer,
    OrderDeliveryLineSerializer,
    OrderDeliveryRetrieveSerializer,
    OrderDeliverySerializer,
)


class OrderDeliveryViewSet(ModelViewSet):
    """
    ViewSet for managing Order Deliveries.
    Provides CRUD operations for OrderDelivery, OrderDeliveryLine, and OrderDeliveryBill.
    """

    queryset = OrderDelivery.objects.all()
    serializer_class = OrderDeliverySerializer

    def get_queryset(self):
        return self.queryset.select_related("order", "bill").prefetch_related("delivery_lines")

    def generate_tracking_number(self):
        date_part = datetime.now().strftime("%Y%m%d")
        random_part = "".join(random.choices(string.ascii_uppercase, k=5))
        return f"{date_part}{random_part}"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["tracking_number"] = self.generate_tracking_number()
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderDeliveryRetrieveSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.get("partial", False)  # Check if partial update is allowed
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.validated_data.get("delivery_status") == OrderStatusChoice.SHIPPED:
            serializer.validated_data["shipped_date"] = datetime.now().date()
        if serializer.validated_data.get("delivery_status") == OrderStatusChoice.DELIVERED:
            serializer.validated_data["delivery_date"] = datetime.now().date()
            # create delivery bill
            OrderDeliveryBill.objects.create(order_delivery=serializer.instance, total_amount=instance.total_amount)
        serializer.save()
        return Response(serializer.data)


class OrderDeliveryLineViewSet(ModelViewSet):
    """
    ViewSet for managing Order Delivery Lines.
    Provides CRUD operations for OrderDeliveryLine.
    """

    queryset = OrderDeliveryLine.objects.all()
    serializer_class = OrderDeliveryLineSerializer

    def get_queryset(self):
        return self.queryset.select_related("order_delivery", "order_line").prefetch_related(
            "order_delivery__delivery_lines"
        )


class OrderDeliveryBillViewSet(ModelViewSet):
    """
    ViewSet for managing Order Delivery Bills.
    Provides CRUD operations for OrderDeliveryBill.
    """

    queryset = OrderDeliveryBill.objects.all()
    serializer_class = OrderDeliveryBillSerializer

    def get_queryset(self):
        return self.queryset.select_related("order_delivery").prefetch_related("order_delivery__delivery_lines")
