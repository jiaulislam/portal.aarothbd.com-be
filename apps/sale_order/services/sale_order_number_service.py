from datetime import date

from django.http import Http404

from core.services import BaseModelService

from ..constants import SaleOrderPrefixChoices
from ..models import SaleOrderSequence


class SaleOrderNumberService(BaseModelService[SaleOrderSequence]):
    model_class = SaleOrderSequence

    def get_sale_order_sequence(self, prefix: SaleOrderPrefixChoices, _date: date) -> SaleOrderSequence:
        try:
            sequence = self.get(prefix=prefix, sequence_date=_date)
        except Http404:
            sequence = self.create({"prefix": prefix, "sequence_date": _date})

        sequence.counter += 1
        sequence.save()
        return sequence
