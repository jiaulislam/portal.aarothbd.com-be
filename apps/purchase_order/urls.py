from django.urls import path

from .views import PurchaseOrderListCreateView

urlpatterns = [
    path(r"purchase-orders/", PurchaseOrderListCreateView.as_view(), name="purchase-order-list-create"),
]
