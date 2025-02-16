from core.services import BaseModelService

from ..models import Cupon

__all__ = ["CuponService"]


class CuponService(BaseModelService[Cupon]):
    model_class = Cupon

    def get_valid_cupons(self, **kwargs):
        queryset = self.model_class.objects.filter(is_active=True, **kwargs)
        return queryset
