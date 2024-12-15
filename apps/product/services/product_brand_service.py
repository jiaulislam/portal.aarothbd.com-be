from typing import Any, MutableMapping

from core.services import BaseModelService

from ..models.product_brand_model import ProductBrand

__all__ = ["ProductBrandService"]


class ProductBrandService(BaseModelService[ProductBrand]):
    model_class = ProductBrand

    def get_or_create(self, brand: MutableMapping[str, Any], **kwargs):
        user = self.core_service.get_user(kwargs.get("request"))
        instance, created = self.model_class.objects.get_or_create(defaults={"name": brand.get("name")})
        if created:
            instance.created_by = user  # type: ignore
            instance.save()
        return instance, created
