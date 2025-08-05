from django.urls import path

from .views import PurchaseOrderListCreateView, PurchaseOrderRetrieveView

urlpatterns = [
    path(r"purchase-orders/", PurchaseOrderListCreateView.as_view(), name="purchase-order-list-create"),
    path(r"purchase-orders/<int:id>/", PurchaseOrderRetrieveView.as_view(), name="purchase-order-retrieve"),
]
