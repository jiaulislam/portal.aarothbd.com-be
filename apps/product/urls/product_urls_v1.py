from django.urls import path

from ..views.product_view_v1 import ProductListCreateAPIView, ProductRetrieveUpdateAPIView, ProductUpdateStatusAPIView

urlpatterns = [
    path(r"products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path(r"products/<str:slug>/", ProductRetrieveUpdateAPIView.as_view(), name="product-update-retrieve"),
    path(r"products/<str:slug>/update-status/", ProductUpdateStatusAPIView.as_view(), name="product-update-status"),
]
