from typing import Any, List, MutableMapping

from core.services import BaseModelService

from ..models.product_model import Product, ProductDetail

__all__ = ["ProductService"]


class ProductService(BaseModelService[Product]):
    model_class = Product
    detail_model_class = ProductDetail

    def update_product_details(self, product: Product, validated_data_list: List[MutableMapping[str, Any]], **kwargs):
        user = self.core_service.get_user(kwargs.get("request"))
        instance = product.details.first()
        if instance:
            for validated_data in validated_data_list:
                for key, value in validated_data.items():
                    setattr(instance, key, value)
                instance.updated_by = user  # type: ignore
                instance.save()
        else:
            self.detail_model_class.objects.create(product=product)
