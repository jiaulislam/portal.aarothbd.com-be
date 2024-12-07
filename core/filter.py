from django_filters import rest_framework as filters


class BaseFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="is_active", lookup_expr="exact")
    created_at = filters.DateRangeFilter(field_name="created_at")
    updated_at = filters.DateRangeFilter(field_name="updated_at")
