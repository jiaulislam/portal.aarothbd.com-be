from django.db import models


class SaleOrderPrefixChoices(models.TextChoices):
    CUSTOMER = "CSO", "Customer Sale Order"
    PAIKAR = "PSO", "Paikar Sale Order"


class SaleOrderStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    APPROVAL_PENDING = "pending_approval", "Pending Approval"
    APPROVED = "approved", "Approved"
    CANCELLED = "cancelled", "Cancelled"
    REJECTED = "rejected", "Rejected"
    DELIVERED = "delivered", "Delivered"
    INVOICED = "invoiced", "Invoiced"
    PAID = "paid", "Paid"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"


class DiscountTypeChoices(models.TextChoices):
    PERCENTAGE = "percentage", "Percentage"
    FIXED = "fixed", "Fixed"
