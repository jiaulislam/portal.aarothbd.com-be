import os
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from apps.company.models import Company
    from apps.product.models import ProductImage

__all__ = [
    "upload_product_image",
    "upload_company_image",
]


def get_upload_file_path(file_name_with_extension, storage_path):
    file_name = f"{uuid4().hex[:8]}_{file_name_with_extension}"
    return os.path.join(storage_path, file_name)


def upload_product_image(instance: "ProductImage", file_name: str):
    """
    Upload product images, uploading folder will be created, if not exist.
    """
    storage_path = "product-images"

    if instance.sale_order:
        storage_path = f"{storage_path}/{instance.sale_order.company.slug}"

    return get_upload_file_path(file_name, storage_path)


def upload_company_image(instance: "Company", file_name: str):
    """
    Upload company images, uploading folder will be created, if not exist.
    """
    storage_path = "company-images"

    if instance:
        storage_path = f"{storage_path}/{instance.slug}"

    return get_upload_file_path(file_name, storage_path)
