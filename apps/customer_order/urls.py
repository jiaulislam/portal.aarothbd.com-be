from django.urls import path

from .views.order_views_v1 import (
    OrderListCreateAPIView,
    OrderPaymentListAPIView,
    OrderPaymentListCreateAPIView,
    OrderRetrieveAPIView,
    OrderUpdateStatusAPIView,
)

urlpatterns = [
    path(r"orders/<int:id>/payments/", OrderPaymentListCreateAPIView.as_view(), name="order-payment-list-create"),
    path(r"payments/", OrderPaymentListAPIView.as_view(), name="order-payment-list"),
    path(r"orders/", OrderListCreateAPIView.as_view(), name="order-list-create"),
    path(r"orders/<int:id>/", OrderRetrieveAPIView.as_view(), name="order-retrieve"),
    path(r"orders/<int:id>/update-status/", OrderUpdateStatusAPIView.as_view(), name="order-update-status"),
]
