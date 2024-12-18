from core.services import BaseModelService

from ..models.product_category_model import ProductCategory


class ProductCategoryService(BaseModelService[ProductCategory]):
    model_class = ProductCategory
