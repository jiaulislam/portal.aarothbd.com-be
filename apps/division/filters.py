from core.filter import BaseFilter

from .models import Division


class DivisionFilter(BaseFilter):
    class Meta:
        model = Division
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
