from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.delivery_views import OrderDeliveryBillViewSet, OrderDeliveryLineViewSet, OrderDeliveryViewSet
from .views.order_views_v1 import (
    OrderListCreateAPIView,
    OrderPaymentListAPIView,
    OrderPaymentListCreateAPIView,
    OrderPaymentReversalAPIView,
    OrderPaymentUpdateAPIView,
    OrderRetrieveUpdateAPIView,
    OrderUpdateStatusAPIView,
)

order_delivery_routers = DefaultRouter()
order_delivery_routers.register(r"deliveries", OrderDeliveryViewSet, basename="order-delivery")
order_delivery_routers.register(r"delivery-lines", OrderDeliveryLineViewSet, basename="order-delivery-line")
order_delivery_routers.register(r"delivery-bills", OrderDeliveryBillViewSet, basename="order-delivery-bill")

urlpatterns = [
    path(
        r"orders/<int:order_id>/payments/",
        OrderPaymentListCreateAPIView.as_view(),
        name="order-payment-list-create",
    ),
    path(
        r"payments/<int:id>/reversal/",
        OrderPaymentReversalAPIView.as_view(),
        name="order-payment-reversal",
    ),
    path(r"payments/", OrderPaymentListAPIView.as_view(), name="order-payment-list"),
    path(
        r"payments/<int:id>/",
        OrderPaymentUpdateAPIView.as_view(),
        name="order-payment-update",
    ),
    path(r"orders/", OrderListCreateAPIView.as_view(), name="order-list-create"),
    path(r"orders/<int:id>/", OrderRetrieveUpdateAPIView.as_view(), name="order-retrieve"),
    path(
        r"orders/<int:id>/update-status/",
        OrderUpdateStatusAPIView.as_view(),
        name="order-update-status",
    ),
    # router urls
    *order_delivery_routers.urls,
]
