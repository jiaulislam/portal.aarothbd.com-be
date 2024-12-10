from core.filter import BaseFilter

from .models import SubDistrict


class SubDistrictFilter(BaseFilter):
    class Meta:
        model = SubDistrict
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
