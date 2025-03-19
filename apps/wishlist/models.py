from datetime import date
from logging import getLogger
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Upper

from apps.sale_order.constants import SaleOrderStatusChoices
from apps.sale_order.models import PaikarSaleOrder
from core.models import BaseModel

if TYPE_CHECKING:
    from apps.company.models import Company
    from apps.product.models.product_model import Product

User = get_user_model()

_logger = getLogger(__name__)


class Wishlist(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")

    def __str__(self) -> str:
        return f"Wishlist for {str(self.user)}"

    def add_product(self, product: "Product", company: "Company") -> None:
        if not self.items.filter(product=product, company=company).exists():
            WishlistItem.objects.create(wishlist=self, product=product, company=company)

    def remove_product(self, product: "Product", company: "Company"):
        self.items.filter(product=product, company=company).delete()

    def get_wishlist_active_sale_orders(self, user):
        """
        Returns:
            QuerySet: A queryset of PaikarSaleOrder objects that match the criteria.
        """
        today = date.today()
        wishlist_items = self._get_wishlist_items(user)
        sale_orders = self._get_sale_orders(wishlist_items, today)
        return sale_orders

    def _get_wishlist_items(self, user):
        """
        Returns:
            QuerySet: A queryset of wishlist items.
        """
        items = self.items.filter(wishlist__user=user).values_list("product", "company", named=True)
        return items

    def _get_sale_orders(self, wishlist_items, today):
        """
        Args:
            wishlist_items (QuerySet): A queryset of wishlist items.
            today (date): The current date.

        Returns:
            QuerySet: A queryset of PaikarSaleOrder objects that match the criteria.
        """
        if not wishlist_items.count():
            # wishlist is empty
            return PaikarSaleOrder.objects.none()

        or_query = Q()
        for item in wishlist_items:
            or_query |= Q(product_id=item.product, company_id=item.company)

        queryset = (
            PaikarSaleOrder.objects.annotate(upper_bound=Upper(F("validity_dates")))  # Extract upper bound
            .exclude(validity_dates__upper_inf=True)  # Exclude infinite upper bound
            .filter(
                or_query,
                status=SaleOrderStatusChoices.APPROVED,  # Ensure order is approved
                upper_bound__gte=today,  # Check if upper bound is >= today
            )
            .select_related("product", "company")
            .prefetch_related("orderlines", "orderlines__uom")
        )

        _logger.debug(queryset.query)

        return queryset

    items: models.QuerySet["WishlistItem"]

    class Meta:
        db_table = "wishlist_wishlist"
        verbose_name = "Wishlist"
        verbose_name_plural = "Users Wishlist"


class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.CASCADE,
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wishlist_wishlist_item"
        unique_together = ("wishlist", "product", "company")

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user}'s wishlist"
