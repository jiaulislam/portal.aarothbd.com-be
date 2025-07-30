from celery import shared_task

from apps.product.services.product_import_service import ProductImportService


@shared_task
def import_products_from_file(file_full_path):
    return ProductImportService.import_products(file_full_path)
