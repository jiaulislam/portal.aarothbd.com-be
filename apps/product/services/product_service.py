from core.services import BaseModelService

from ..models.product_model import Product

__all__ = ["ProductService"]


class ProductService(BaseModelService):
    model_class = Product
