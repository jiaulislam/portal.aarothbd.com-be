from django.urls import path

from .views.order_views_v1 import OrderListCreateAPIView, OrderRetrieveAPIView

urlpatterns = [
    path(r"orders/", OrderListCreateAPIView.as_view(), name="order-list-create"),
    path(r"orders/<int:id>/", OrderRetrieveAPIView.as_view(), name="order-retrieve"),
]
