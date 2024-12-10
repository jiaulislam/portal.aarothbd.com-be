from core.filter import BaseFilter

from .models import District


class DistrictFilter(BaseFilter):
    class Meta:
        model = District
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
