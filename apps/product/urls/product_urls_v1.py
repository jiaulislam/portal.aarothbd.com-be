from django.urls import path

from ..views.product_brand_view_v1 import ProductBrandListCreateAPIView
from ..views.product_category_view_v1 import (
    ProductCategoryListCreateAPIView,
    ProductCategoryRetrieveUpdateAPIView,
    ProductCategoryUpdateStatusAPIView,
)
from ..views.product_view_v1 import ProductListCreateAPIView, ProductRetrieveUpdateAPIView, ProductUpdateStatusAPIView

urlpatterns = [
    path(r"products/categories/", ProductCategoryListCreateAPIView.as_view(), name="product-category-list-create"),
    path(
        r"products/categories/<int:id>/",
        ProductCategoryRetrieveUpdateAPIView.as_view(),
        name="product-category-retrieve-update",
    ),
    path(
        r"products/categories/<int:id>/update-status/",
        ProductCategoryUpdateStatusAPIView.as_view(),
        name="product-category-udpate-status",
    ),
    path(r"products/brands/", ProductBrandListCreateAPIView.as_view(), name="product-brands-list-create"),
    path(r"products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path(r"products/<str:slug>/", ProductRetrieveUpdateAPIView.as_view(), name="product-update-retrieve"),
    path(r"products/<str:slug>/update-status/", ProductUpdateStatusAPIView.as_view(), name="product-update-status"),
]
