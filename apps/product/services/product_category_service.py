from django.db.models import Prefetch, Q, QuerySet
from django.http import Http404

from core.services import BaseModelService

from ..models.product_category_model import ProductCategory


class ProductCategoryService(BaseModelService[ProductCategory]):
    model_class = ProductCategory

    def get_parent_categories(self) -> QuerySet[ProductCategory]:
        queryset = self.model_class.objects.filter(
            parent__isnull=True,
        ).prefetch_related(
            Prefetch(
                "child_product_categories",
                queryset=self.model_class.objects.select_related("parent"),
                to_attr="childrens",
            )
        )
        return queryset

    def find_by_id_or_parent_id(self, id: int) -> ProductCategory:
        instance = (
            self.model_class.objects.filter(Q(id=id) | Q(parent_id=id))
            .prefetch_related(Prefetch("child_product_categories", to_attr="childrens"))
            .first()
        )
        if not instance:
            raise Http404(f"category not found for id or parent_id {id}")
        return instance
