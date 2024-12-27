from django_filters import filters

from core.constants.common import COMMON_EXCLUDE_FIELDS
from core.filter import BaseFilter

from .models import UoM, UoMCategory


class UoMCategoryFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = UoMCategory
        exclude = COMMON_EXCLUDE_FIELDS


class UoMFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = UoM
        exclude = COMMON_EXCLUDE_FIELDS
