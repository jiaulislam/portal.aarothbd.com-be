from django.db.models import TextChoices


class OrderStatusChoice(TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"


class PaymodeChoice(TextChoices):
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY", "Cash on Delivery"
    ONLINE_PAYMENT = "ONLINE_PAYMENT", "Online Payment"
