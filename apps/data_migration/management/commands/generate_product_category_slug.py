from django.core.management.base import BaseCommand
from django.db import transaction

from apps.product.models import ProductCategory


class Command(BaseCommand):
    help = "Migrate Existing Product Category to generate slug"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            categories = ProductCategory.objects.all()
            for category in categories:
                category.save()
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found !"))
