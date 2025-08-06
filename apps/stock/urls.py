from django.urls import path

from .views import StockListCreateView, StockMovementListCreateView, StockMovementRetrieveView, StockRetrieveView

urlpatterns = [
    path("stocks/", StockListCreateView.as_view(), name="stock-list-create"),
    path("stocks/<int:id>/", StockRetrieveView.as_view(), name="stock-retrieve"),
    path("stock-movements/", StockMovementListCreateView.as_view(), name="stock-movement-list-create"),
    path("stock-movements/<int:id>/", StockMovementRetrieveView.as_view(), name="stock-movement-retrieve"),
]
