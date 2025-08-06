from django.contrib import admin

from core.admin import BaseAdmin

from .models import Stock, StockMovement


@admin.register(Stock)
class StockAdmin(BaseAdmin):
    list_display = ("product", "company", "quantity", "trade_price", "mrp", "last_updated")
    search_fields = ("product__name", "company__name")
    list_filter = ("company",)
    ordering = ("-last_updated",)


@admin.register(StockMovement)
class StockMovementAdmin(BaseAdmin):
    list_display = ("stock", "movement_type", "quantity", "previous_quantity", "new_quantity", "created_at")
    search_fields = ("stock__product__name", "stock__company__name")
    list_filter = ("movement_type",)
    ordering = ("-created_at",)
