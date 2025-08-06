from django.db import models

from .constants import StockMovementType


class InStockMovementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(movement_type=StockMovementType.IN)


class OutStockMovementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(movement_type=StockMovementType.OUT)
