from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import OrderLine
from ..serializers.order_line_serializer import OrderLineCreateUpdateSerializer


class OrderLineUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    http_method_names = ["delete", "patch"]

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")
        return self.queryset.filter(order_id=order_id)
