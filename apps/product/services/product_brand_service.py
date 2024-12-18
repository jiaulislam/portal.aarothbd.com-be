from typing import Any, MutableMapping

from core.services import BaseModelService

from ..models.product_brand_model import ProductBrand

__all__ = ["ProductBrandService"]


class ProductBrandService(BaseModelService[ProductBrand]):
    model_class = ProductBrand

    def get_or_create(self, brand: MutableMapping[str, Any], **kwargs):
        created = False
        user = self.core_service.get_user(kwargs.get("request"))
        instance = self.model_class.objects.filter(name=brand.get("name")).first()
        if not instance:
            instance = self.model_class.objects.create(**brand)
            instance.created_by = user  # type: ignore
            created = True
            instance.save()
        return instance, created
