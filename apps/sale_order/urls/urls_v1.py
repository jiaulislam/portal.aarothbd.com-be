from django.urls import path

from ..views.paikar_sale_order_view_v1 import PaikarSaleOrderListCreateAPIView, PaikarSaleOrderRetrieveUpdateAPIView

urlpatterns = [
    path("paikar/sale-orders/<int:id>/", PaikarSaleOrderRetrieveUpdateAPIView.as_view(),
         name="paikar-sale-order-retrieve-update"),
    path("paikar/sale-orders/", PaikarSaleOrderListCreateAPIView.as_view(), name="paikar-sale-order-list-create"),
]
