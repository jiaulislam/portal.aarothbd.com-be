from django.utils import timezone

from core.request import Request
from core.services import BaseModelService

from ..models import Offer

__all__ = ["OfferService"]


class OfferService(BaseModelService[Offer]):
    model_class = Offer

    def get_valid_offers(self, **kwargs):
        _today = timezone.now().date()
        queryset = self.model_class.objects.filter(end_date__date__gte=_today, **kwargs)
        return queryset

    def accept_offer_agreement(self, instance: Offer, **kwargs) -> Offer:
        """accept offer agreement for given offer instance"""
        request: Request | None = kwargs.get("request")
        instance.company_agreed = True
        instance.agreed_by = request.user if request else None
        instance.agreed_at = timezone.now()
        instance.save()
        return instance
