from django.utils import timezone

from core.services import BaseModelService

from ..models import Offer

__all__ = ["OfferService"]


class OfferService(BaseModelService[Offer]):
    model_class = Offer

    def get_valid_offers(self, **kwargs):
        _today = timezone.now().date()
        queryset = self.model_class.objects.filter(is_active=True, end_date__date__gte=_today, **kwargs)
        return queryset
