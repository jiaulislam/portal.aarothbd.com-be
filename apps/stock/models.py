from typing import TYPE_CHECKING, Iterable, List

from django.db import models

from core.models import BaseModel

from .constants import StockMovementType, StockReferenceType

if TYPE_CHECKING:
    from apps.company.models import Company
    from apps.product.models import Product


class StockMovement(BaseModel):
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, related_name="movements", verbose_name="Stock")
    movement_type = models.CharField(max_length=20, choices=StockMovementType.choices, verbose_name="Movement Type")
    quantity = models.IntegerField(verbose_name="Quantity")  # Can be positive or negative
    previous_quantity = models.PositiveIntegerField(verbose_name="Previous Quantity")
    new_quantity = models.PositiveIntegerField(verbose_name="New Quantity")
    reference_type = models.CharField(max_length=50, choices=StockReferenceType.choices, verbose_name="Reference Type")
    reference_id = models.PositiveIntegerField(verbose_name="Reference ID")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")

    def __str__(self):
        return f"{self.stock} - {self.movement_type} - {self.quantity}"

    class Meta:
        db_table = "stock_stock_movement"
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"
        ordering = ["-created_at"]


class Stock(BaseModel):
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="stocks", verbose_name="Product"
    )
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="stocks", verbose_name="Company"
    )
    mrp = models.FloatField(default=0.0, verbose_name="MRP")
    trade_price = models.FloatField(default=0.0, verbose_name="Trade Price")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    @staticmethod
    def create_default_stock(company: "Company", products: Iterable["Product"]) -> List["Stock"]:
        """
        Creates default stock entries for a list of products within a specified company.

        For each product provided, this function ensures that a corresponding Stock object exists for the given company.
        If a Stock entry does not already exist, it is created with default values for MRP, trade price, and quantity
        (all set to 0).

        Args:
            company (Company): The company for which stock entries are to be created.
            products (Iterable[Product]): An iterable of Product instances to create stock entries for.

        Returns:
            List[Stock]: A list of Stock objects corresponding to the provided products.
        """
        stocks = []
        for product in products:
            stock, _ = Stock.objects.get_or_create(
                product=product, company=company, defaults={"mrp": 0.0, "trade_price": 0.0, "quantity": 0}
            )
            stocks.append(stock)
        return stocks

    def update_stock_quantity(
        self,
        quantity: int,
        reference_type: StockReferenceType = StockReferenceType.ADJUSTMENT,
        reference_id: int = None,
        notes: str = None,
    ) -> int:
        """
        Update the stock quantity for the product in the specified company.
        Supports both increasing (positive quantity) and decreasing (negative quantity) stock.

        Args:
            quantity (int): The quantity to add/subtract. Positive to increase, negative to decrease.
            reference_type (str): Type of reference for this movement.
            reference_id (int): ID of the reference object.
            notes (str): Optional notes for this movement.

        Raises:
            ValueError: If the operation would result in negative stock or if quantity is zero.
        Returns:
            int: The new stock quantity after the operation.
        """
        if quantity == 0:
            raise ValueError("Quantity change cannot be zero.")

        previous_quantity = self.quantity
        new_quantity = self.quantity + quantity

        if new_quantity < 0:
            raise ValueError(
                f"Insufficient stock to perform this operation. "
                f"Current stock: {self.quantity}, Requested change: {quantity}, "
                f"Would result in: {new_quantity}"
            )

        self.quantity = new_quantity
        self.save(update_fields=["quantity", "last_updated"])

        # Create stock movement record
        movement_type = StockMovementType.IN if quantity > 0 else StockMovementType.OUT
        StockMovement.objects.create(
            stock=self,
            movement_type=movement_type,
            quantity=quantity,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
        )

        return self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.company.name} - {self.quantity}"

    class Meta:
        db_table = "stock_stock"
        unique_together = ("product", "company")
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
