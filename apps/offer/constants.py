from django.db import models


class DiscountPriceMode(models.TextChoices):
    FIXED = "fixed", "Fixed"
    PERCENTAGE = "percentage", "Percentage"
