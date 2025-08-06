from django_filters import rest_framework as filters

from core.filter import BaseFilter

from .models import PurchaseOrder


class PurchaseOrderFilter(BaseFilter):
    entry_type = filters.ChoiceFilter(
        choices=[
            ("PO", "Purchase Order"),
            ("PR", "Purchase Return"),
        ],
        field_name="entry_type",
        lookup_expr="exact",
    )
    supplier = filters.CharFilter(field_name="supplier__name", lookup_expr="icontains")
    supplier_id = filters.NumberFilter(field_name="supplier__id")

    order_date_from = filters.DateFilter(field_name="order_date", lookup_expr="gte")
    order_date_to = filters.DateFilter(field_name="order_date", lookup_expr="lte")
    order_date = filters.DateFromToRangeFilter(field_name="order_date")

    created_at_from = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at_to = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")

    product = filters.CharFilter(field_name="order_lines__product__name", lookup_expr="icontains")
    product_id = filters.NumberFilter(field_name="order_lines__product__id")

    order_number = filters.CharFilter(field_name="order_number", lookup_expr="icontains")

    class Meta:
        model = PurchaseOrder
        fields = {
            "supplier": ["exact"],
            "order_date": ["exact", "gte", "lte"],
            "created_at": ["exact", "gte", "lte"],
        }
