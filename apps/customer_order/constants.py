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


class PaymentMethodChoice(TextChoices):
    CASH = "CASH", "Cash"
    CARD = "CARD", "Card"
    MFS = "MFS", "MFS"
    BANK = "BANK", "Bank Draft"
    RTGS = "RTGS", "RTGS"
    CHEQUE = "CHEQUE", "Cheque"
    BEFTN = "BEFTN", "BEFTN"


class PaymentStatusChoice(TextChoices):
    PAID = "paid", "Paid"
    UNPAID = "unpaid", "Unpaid"
    PARTIAL = "partial", "Partial"
