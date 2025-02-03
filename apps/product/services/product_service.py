from typing import Any, List, MutableMapping

from django.db.models import Exists, OuterRef, Prefetch

from core.services import BaseModelService

from ..models.product_model import Product, ProductDetail

__all__ = ["ProductService"]


class ProductService(BaseModelService[Product]):
    model_class = Product
    detail_model_class = ProductDetail

    def create_product_details(self, product: Product, validated_data_list: List[MutableMapping[str, Any]], **kwargs):
        user = self.core_service.get_user(kwargs.get("request"))
        details_list = []
        for validated_data in validated_data_list:
            validated_data["created_by"] = user
            validated_data["updated_by"] = user
            validated_data["product"] = product
            details_list.append(ProductDetail(**validated_data))
        self.detail_model_class.objects.bulk_create(details_list)

    def update_product_details(self, product: Product, validated_data_list: List[MutableMapping[str, Any]], **kwargs):
        product.details.delete()
        self.create_product_details(product, validated_data_list, request=kwargs.get("request"))

    def get_ecom_queryset(self):
        from apps.sale_order.constants import SaleOrderStatusChoices
        from apps.sale_order.models import PaikarSaleOrder

        # ✅ Subquery: Checks if an approved sale order exists for the product
        approved_orders = PaikarSaleOrder.objects.filter(product=OuterRef("pk"), status=SaleOrderStatusChoices.APPROVED)

        # ✅ Separate queryset for prefetching (without OuterRef) as we cannot use it inside subquery
        approved_orders_prefetch = PaikarSaleOrder.objects.filter(status=SaleOrderStatusChoices.APPROVED)

        queryset = self.model_class.objects.filter(
            Exists(approved_orders),
        ).prefetch_related(
            Prefetch(
                "paikar_sale_orders",
                queryset=approved_orders_prefetch,
                to_attr="paikar_sale_order_product",
            )
        )
        return queryset
