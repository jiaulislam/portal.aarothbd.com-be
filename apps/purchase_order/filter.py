import django_filters

from .models import PurchaseOrder


class PurchaseOrderFilter(django_filters.FilterSet):
    supplier = django_filters.CharFilter(field_name="supplier__name", lookup_expr="icontains")
    supplier_id = django_filters.NumberFilter(field_name="supplier__id")

    order_date_from = django_filters.DateFilter(field_name="order_date", lookup_expr="gte")
    order_date_to = django_filters.DateFilter(field_name="order_date", lookup_expr="lte")
    order_date = django_filters.DateFromToRangeFilter(field_name="order_date")

    created_at_from = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at_to = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")

    product = django_filters.CharFilter(field_name="order_lines__product__name", lookup_expr="icontains")
    product_id = django_filters.NumberFilter(field_name="order_lines__product__id")

    order_number = django_filters.CharFilter(field_name="order_number", lookup_expr="icontains")

    class Meta:
        model = PurchaseOrder
        fields = {
            "supplier": ["exact"],
            "order_date": ["exact", "gte", "lte"],
            "created_at": ["exact", "gte", "lte"],
        }
