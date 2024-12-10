from core.filter import BaseFilter

from .models import Country


class CountryFilter(BaseFilter):
    class Meta:
        model = Country
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
