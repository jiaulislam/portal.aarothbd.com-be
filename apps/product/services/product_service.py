from core.services import BaseModelService

from ..models.product_model import Product

__all__ = ["ProductService"]


class ProductService(BaseModelService[Product]):
    model_class = Product
