from django.urls import path

from .views import PurchaseOrderLineDestroyAPIView, PurchaseOrderListCreateView, PurchaseOrderRetrieveView

urlpatterns = [
    path(r"purchase-orders/", PurchaseOrderListCreateView.as_view(), name="purchase-order-list-create"),
    path(r"purchase-orders/<int:id>/", PurchaseOrderRetrieveView.as_view(), name="purchase-order-retrieve"),
    path(
        r"purchase-order-lines/<int:id>/", PurchaseOrderLineDestroyAPIView.as_view(), name="purchase-order-line-destroy"
    ),
]
