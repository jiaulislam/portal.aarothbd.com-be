from datetime import date
from typing import TYPE_CHECKING, Any, List, MutableMapping

from django.db.models import F
from django.db.models.functions import Upper

from core.services import BaseModelService

from ..models.product_model import Product, ProductDetail

if TYPE_CHECKING:
    from apps.company.models import Company

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

        today = date.today()
        # ✅ Subquery: Checks if an approved sale order exists for the product
        # TODO: as per @hridoy he wants to have the validity date as configuration options
        # so to do this we need to introduce a configuration model for the central admin.
        # then it should be controlled from there. Then the query need to do refactor.
        approved_orders = (
            PaikarSaleOrder.objects.annotate(upper_bound=Upper(F("validity_dates")))
            .exclude(validity_dates__upper_inf=True)
            .filter(status=SaleOrderStatusChoices.APPROVED, upper_bound__gte=today)
        )
        return approved_orders

    def get_company_product_sale_orders(self, company: "Company"):
        from apps.sale_order.constants import SaleOrderStatusChoices
        from apps.sale_order.models import PaikarSaleOrder

        today = date.today()
        allowed_products = company.allowed_products.values_list("id", flat=True)

        sale_orders = (
            PaikarSaleOrder.objects.annotate(upper_bound=Upper(F("validity_dates")))  # Extract upper bound
            .exclude(validity_dates__upper_inf=True)  # Exclude infinite upper bound
            .filter(
                product__in=allowed_products,
                company=company,
                status=SaleOrderStatusChoices.APPROVED,  # Ensure order is approved
                upper_bound__gte=today,  # Check if upper bound is >= today
            )
        )

        return sale_orders
