from django.db.models import TextChoices


class StockMovementType(TextChoices):
    IN = "IN", "Stock In"
    OUT = "OUT", "Stock Out"
    ADJUSTMENT = "ADJUSTMENT", "Stock Adjustment"


class StockReferenceType(TextChoices):
    PURCHASE_ORDER = "PURCHASE_ORDER", "Purchase Order"
    SALE_ORDER = "SALE_ORDER", "Sale Order"
    ADJUSTMENT = "ADJUSTMENT", "Manual Adjustment"
    PURCHASE_RETURN = "PURCHASE_RETURN", "Purchase Return"
