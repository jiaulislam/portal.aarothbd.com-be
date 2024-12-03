from django_filters import rest_framework as filters


class UserFilterSet(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="is_active", lookup_expr="exact")
