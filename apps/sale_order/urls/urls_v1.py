from django.urls import path

from ..views import ReviewCreateAPIView
from ..views.paikar_sale_order_view_v1 import (
    PaikarSaleOrderApprovalAPIView,
    PaikarSaleOrderListCreateAPIView,
    PaikarSaleOrderRetrieveUpdateAPIView,
)

urlpatterns = [
    path(
        "paikar/sale-orders/<int:id>/",
        PaikarSaleOrderRetrieveUpdateAPIView.as_view(),
        name="paikar-sale-order-retrieve-update",
    ),
    path("paikar/sale-orders/", PaikarSaleOrderListCreateAPIView.as_view(), name="paikar-sale-order-list-create"),
    path(
        "paikar/sale-orders/<int:id>/approve/",
        PaikarSaleOrderApprovalAPIView.as_view(),
        name="paikar-sale-order-approve",
    ),
    # TODO: Need to refactor the product review to products as this is conflicting URL.
    path(
        r"product-reviews/",
        ReviewCreateAPIView.as_view(),
        name="product-reviews-create-view",
    ),
]
