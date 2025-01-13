from django.db.models import Q, QuerySet
from django.http import Http404

from core.services import BaseModelService

from ..models.product_category_model import ProductCategory


class ProductCategoryService(BaseModelService[ProductCategory]):
    model_class = ProductCategory

    def get_parent_categories(self) -> QuerySet[ProductCategory]:
        return self.model_class.objects.filter(parent__isnull=True).select_related("parent")

    def find_by_id_or_parent_id(self, id: int) -> ProductCategory:
        instance = self.model_class.objects.filter(Q(id=id) | Q(parent_id=id)).first()
        if not instance:
            raise Http404(f"category not found for id or parent_id {id}")
        return instance
