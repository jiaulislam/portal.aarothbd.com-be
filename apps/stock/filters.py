from django_filters import rest_framework as filters

from core.filter import BaseFilter

from .models import Stock, StockMovement


class StockFilter(BaseFilter):
    product = filters.CharFilter(field_name="product__name", lookup_expr="icontains")
    product_id = filters.NumberFilter(field_name="product__id")
    company = filters.CharFilter(field_name="company__name", lookup_expr="icontains")
    company_id = filters.NumberFilter(field_name="company__id")
    quantity_min = filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = filters.NumberFilter(field_name="quantity", lookup_expr="lte")
    mrp_min = filters.NumberFilter(field_name="mrp", lookup_expr="gte")
    mrp_max = filters.NumberFilter(field_name="mrp", lookup_expr="lte")
    trade_price_min = filters.NumberFilter(field_name="trade_price", lookup_expr="gte")
    trade_price_max = filters.NumberFilter(field_name="trade_price", lookup_expr="lte")
    last_updated_after = filters.DateTimeFilter(field_name="last_updated", lookup_expr="gte")
    last_updated_before = filters.DateTimeFilter(field_name="last_updated", lookup_expr="lte")

    class Meta:
        model = Stock
        fields = [
            "product",
            "product_id",
            "company",
            "company_id",
            "quantity_min",
            "quantity_max",
            "mrp_min",
            "mrp_max",
            "trade_price_min",
            "trade_price_max",
            "last_updated_after",
            "last_updated_before",
        ]


class StockMovementFilter(BaseFilter):
    stock = filters.NumberFilter(field_name="stock__id")
    product = filters.CharFilter(field_name="stock__product__name", lookup_expr="icontains")
    company = filters.CharFilter(field_name="stock__company__name", lookup_expr="icontains")
    movement_type = filters.ChoiceFilter(
        choices=[("IN", "Stock In"), ("OUT", "Stock Out"), ("ADJUSTMENT", "Stock Adjustment")]
    )
    reference_type = filters.CharFilter()
    reference_id = filters.NumberFilter()
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    quantity_min = filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = filters.NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model = StockMovement
        fields = [
            "stock",
            "product",
            "company",
            "movement_type",
            "reference_type",
            "reference_id",
            "created_after",
            "created_before",
            "quantity_min",
            "quantity_max",
        ]
