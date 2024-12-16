from core.filter import BaseFilter

from .models.product_model import Product


class ProductFilter(BaseFilter):
    class Meta:
        model = Product
        fields = ("sku_code", "uom", "category", "brand", "origin")
