from django.core.management.base import BaseCommand
from django.db import transaction

from apps.sale_order.models import PaikarSaleOrder


class Command(BaseCommand):
    help = "Migrate Existing Sale Orders to generate slug"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            sale_orders = PaikarSaleOrder.objects.all()
            for sale_order in sale_orders:
                sale_order.save()
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found !"))
