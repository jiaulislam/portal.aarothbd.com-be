from django_filters import rest_framework as filters


class BaseFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="is_active", lookup_expr="exact")
