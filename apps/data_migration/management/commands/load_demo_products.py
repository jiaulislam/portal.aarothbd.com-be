from django.core.management import BaseCommand

from apps.product.tests.factories import (
    PARENT_CATEGORIS,
    ProductBrandFactory,
    ProductCategory,
    ProductCategoryFactory,
    ProductDetailFactory,
    ProductFactory,
)
from core.services import capture_exception_sentry


class Command(BaseCommand):
    help = "Load Demo Products"
    max_instance = 10000

    def handle(self, *args, **options):
        try:
            parent_categories = []
            # create root categories
            for category in PARENT_CATEGORIS:
                parent_categories.append(ProductCategory(name=category, parent=None))
            ProductCategory.objects.bulk_create(parent_categories)

            # create sub categories
            _ = ProductCategoryFactory.create_batch(size=30)

            # create brands
            _ = ProductBrandFactory.create_batch(size=100)

            # create products
            products = ProductFactory.create_batch(self.max_instance)
            for product in products:
                if product.has_detail:
                    _ = ProductDetailFactory.create_instance(product)
        except Exception as e:
            capture_exception_sentry(e)
            raise e
