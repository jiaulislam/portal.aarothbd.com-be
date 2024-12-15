from django.urls import path

from .views import UoMCategoryListCreateAPIView, UoMListCreateAPIView

urlpatterns = [
    path(r"uoms/", UoMListCreateAPIView.as_view(), name="uom-list-create"),
    path(r"uoms/categories/", UoMCategoryListCreateAPIView.as_view(), name="uom-category-list-create"),
]
