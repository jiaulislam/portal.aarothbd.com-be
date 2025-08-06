import random
import string

from django.db import models
from django.utils import timezone

from core.models import BaseModel
from core.request import Request


class EntryType(models.TextChoices):
    PURCHASE_ORDER = "PO", "Purchase Order"
    PURCHASE_RETURN = "PR", "Purchase Return"


class PurchaseOrder(BaseModel):
    order_number = models.CharField(max_length=255, unique=True, verbose_name="Order Number")
    supplier = models.ForeignKey(
        "company.Company", on_delete=models.PROTECT, related_name="purchase_orders", verbose_name="Supplier"
    )
    order_date = models.DateField(verbose_name="Order Date")
    entry_type = models.CharField(max_length=255, default=EntryType.PURCHASE_ORDER, verbose_name="Entry Type")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")

    order_lines: models.QuerySet["PurchaseOrderLine"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            random_chars = "".join(random.choices(string.ascii_uppercase, k=5))
            date_str = self.order_date.strftime("%Y%m%d") if self.order_date else timezone.now().strftime("%Y%m%d")
            if self.entry_type == EntryType.PURCHASE_ORDER:
                self.order_number = f"PO{date_str}{random_chars}"
            elif self.entry_type == EntryType.PURCHASE_RETURN:
                self.order_number = f"PR{date_str}{random_chars}"
        super().save(*args, **kwargs)

    @property
    def total_trade_price(self) -> float:
        return sum(line.total_trade_price for line in self.order_lines.all())

    @property
    def total_margin_amount(self) -> float:
        return sum(line.margin_amount for line in self.order_lines.all())

    @property
    def total_quantity(self) -> int:
        return sum(line.quantity for line in self.order_lines.all())

    @property
    def total_mrp(self) -> float:
        return sum(line.mrp * line.quantity for line in self.order_lines.all())

    def update_stock_quantity(self, request: Request):
        """
        Update the stock quantity of the products in the purchase order.
        This method should be called after the purchase order is created.
        In the ProductStock model, find the stock entry for each product & company in the order lines
        and update the stock quantity accordingly.
        """
        from apps.stock.constants import StockReferenceType
        from apps.stock.models import Stock

        if not request:
            raise ValueError("Request object is required to update stock quantities.")

        for order_line in self.order_lines.all():
            # Get or create stock entry for the product and supplier company
            stock, created = Stock.objects.get_or_create(
                product=order_line.product,
                company=self.supplier,
                defaults={
                    "mrp": order_line.mrp,
                    "trade_price": order_line.trade_price,
                    "quantity": 0,
                    "created_by": request.user,
                    "updated_by": request.user,
                },
            )

            if self.entry_type == EntryType.PURCHASE_ORDER:
                # Update stock prices if this is an existing stock entry
                if not created:
                    stock.mrp = order_line.mrp
                    stock.trade_price = order_line.trade_price
                    stock.updated_by = request.user
                    stock.last_updated = timezone.now()
                    stock.save(update_fields=["mrp", "trade_price", "last_updated", "updated_by"])

                # Increase stock quantity using the Stock model's method
                if order_line.quantity > 0:
                    stock.update_stock_quantity(
                        order_line.quantity,
                        reference_type=StockReferenceType.PURCHASE_ORDER,
                        reference_id=self.id,
                        notes=f"Purchase Order {self.order_number} \
                            - {order_line.product.name} by {str(request.user)}",
                    )

            if self.entry_type == EntryType.PURCHASE_RETURN:
                # Decrease stock quantity using the Stock model's method
                if order_line.quantity > 0:
                    stock.update_stock_quantity(
                        -order_line.quantity,
                        reference_type=StockReferenceType.PURCHASE_RETURN,
                        reference_id=self.id,
                        notes=f"Purchase Return {self.order_number} \
                            - {order_line.product.name} by {str(request.user)}",
                    )

    def __str__(self):
        return f"Purchase Order {self.order_number} - {self.supplier.name}"

    class Meta:
        db_table = "purchase_order_purchase_order"
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"


class PurchaseOrderLine(BaseModel):
    purchase_order = models.ForeignKey(
        "purchase_order.PurchaseOrder", on_delete=models.CASCADE, related_name="order_lines", verbose_name="Order"
    )
    product = models.ForeignKey(
        "product.Product", on_delete=models.PROTECT, related_name="purchase_order_lines", verbose_name="Product"
    )
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    trade_price = models.FloatField(verbose_name="Trade Price", default=0.0)
    mrp = models.FloatField(verbose_name="MRP", default=0.0)

    @property
    def gp_margin(self) -> float:
        if self.mrp > 0:
            return round((self.mrp - self.trade_price) / self.mrp * 100, 2)
        return 0.0

    @property
    def total_trade_price(self) -> float:
        return self.quantity * self.trade_price

    @property
    def margin_amount(self) -> float:
        return self.quantity * (self.mrp - self.trade_price)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"

    class Meta:
        db_table = "purchase_order_purchase_order_line"
        verbose_name = "Purchase Order Line"
        verbose_name_plural = "Purchase Order Lines"
