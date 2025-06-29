from rest_framework.viewsets import ModelViewSet

from ..models import OrderDelivery, OrderDeliveryBill, OrderDeliveryLine
from ..serializers import OrderDeliveryBillSerializer, OrderDeliveryLineSerializer, OrderDeliverySerializer


class OrderDeliveryViewSet(ModelViewSet):
    """
    ViewSet for managing Order Deliveries.
    Provides CRUD operations for OrderDelivery, OrderDeliveryLine, and OrderDeliveryBill.
    """

    queryset = OrderDelivery.objects.all()
    serializer_class = OrderDeliverySerializer

    def get_queryset(self):
        return self.queryset.select_related("order", "bill").prefetch_related("delivery_lines")


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
