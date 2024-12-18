from django.db.models import QuerySet

from core.services import BaseModelService

from ..models.product_category_model import ProductCategory


class ProductCategoryService(BaseModelService[ProductCategory]):
    model_class = ProductCategory

    def get_parent_categories(self) -> QuerySet[ProductCategory]:
        return self.model_class.objects.filter(parent__isnull=True).select_related("parent")
