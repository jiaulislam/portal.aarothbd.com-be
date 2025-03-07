from typing import Any

from rest_framework import serializers as s

from apps.sale_order.models import PaikarSaleOrder
from apps.sale_order.serializers.sale_order_serializer import DateRangeField
from core import utils
from core.constants import AUDIT_COLUMNS

from ..models.product_model import Product, ProductDetail
from .product_brand_serializer import ProductBrandSerializer
from .product_category_serializer import ProductCategorySerializer
from .product_image_serializer import ProductImageSerializer


class ProductDetailSerializer(s.ModelSerializer):
    class Meta:
        model = ProductDetail
        exclude = AUDIT_COLUMNS + ("product", "id")


class ProductSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS


class ProductNestedSerializer(s.ModelSerializer):
    category = s.SerializerMethodField()
    uom = s.SerializerMethodField()
    brand = s.SerializerMethodField()
    origin = s.SerializerMethodField()
    details = ProductDetailSerializer(read_only=True, many=True)
    images = s.SerializerMethodField()

    def get_category(self, obj: Product):
        data = ProductCategorySerializer(instance=obj.category).data
        return data

    def get_uom(self, obj: Product):
        from apps.uom.serializers import UoMSerializer

        data = utils.get_serialized_data(UoMSerializer, obj, "uom")
        return data

    def get_brand(self, obj: Product):
        data = utils.get_serialized_data(ProductBrandSerializer, obj, "brand")
        return data

    def get_origin(self, obj: Product):
        from apps.country.serializers import CountrySerializer

        data = utils.get_serialized_data(CountrySerializer, obj, "origin")
        return data

    def get_images(self, obj: Product):
        queryset = obj.images.filter(is_default=True, sale_order__isnull=True)
        return ProductImageSerializer(queryset, many=True).data

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "sku_code",
            "has_detail",
            "details",
            "attributes",
            "html",
            "uom",
            "category",
            "brand",
            "origin",
            "images",
        )


class ProductExtendedSerializer(s.ModelSerializer):
    brand = ProductBrandSerializer(read_only=True)
    details = ProductDetailSerializer(read_only=True, many=True)
    sale_orders = s.SerializerMethodField()
    uom = s.SerializerMethodField()
    category = s.SerializerMethodField()
    origin = s.SerializerMethodField()

    def get_sale_orders(self, obj: Product):
        from apps.sale_order.serializers import PaikarSaleOrderDetailSerializer

        data = utils.get_serialized_data(PaikarSaleOrderDetailSerializer, obj, "paikar_sale_orders", many=True)
        return data

    def get_uom(self, obj: Product):
        from apps.uom.serializers import UoMSerializer

        data = utils.get_serialized_data(UoMSerializer, obj, "uom")
        return data

    def get_category(self, obj: Product):
        data = utils.get_serialized_data(ProductCategorySerializer, obj, "category")
        return data

    def get_origin(self, obj: Product):
        from apps.country.serializers import CountrySerializer

        data = utils.get_serialized_data(CountrySerializer, obj, "origin")
        return data

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS


class ProductCreateSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(write_only=True, many=True)
    brand = ProductBrandSerializer(write_only=True)

    def to_representation(self, instance: "Product") -> dict[str, Any]:
        response = super().to_representation(instance)
        response["uom"] = instance.uom.name
        response["category"] = instance.category.name
        response["brand"] = instance.brand.name if instance.brand else None
        response["origin"] = instance.origin.name if instance.origin else None
        return response

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS


class ProductUpdateSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(write_only=True, many=True)
    brand = ProductBrandSerializer(write_only=True)

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS
        read_only_fields = ("slug", "id", "sku_code")


class ProductUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = Product
        fields = ("is_active", "id")


class ProductEcomSerializer(s.ModelSerializer):
    product = ProductNestedSerializer(read_only=True)
    company = s.SerializerMethodField()
    validity_dates = DateRangeField()
    orderlines = s.SerializerMethodField()
    reviews = s.SerializerMethodField()
    images = s.SerializerMethodField()

    def get_orderlines(self, obj):
        from apps.sale_order.serializers import SaleOrderLineSerializer

        return utils.get_serialized_data(SaleOrderLineSerializer, obj, "orderlines", many=True)

    def get_company(self, obj):
        from apps.company.serializers.company_serializer_v1 import CompanySerializer

        return utils.get_serialized_data(CompanySerializer, obj, "company")

    def get_reviews(self, obj: PaikarSaleOrder):
        # FIXME: fix this clutter later
        from apps.sale_order.models import Review
        from apps.sale_order.serializers import SaleOrderReviewSerializer

        queryset = (
            Review.objects.filter(
                sale_order__product=obj.product,
                sale_order__company=obj.company,
                is_active=True,
            )
            .all()
            .order_by("-id")
        )
        serializer = SaleOrderReviewSerializer(queryset, many=True)
        return serializer.data

    def get_images(self, obj: PaikarSaleOrder):
        from apps.product.serializers import ProductImageSerializer

        queryset = obj.product.images.filter(sale_order=obj, product=obj.product)
        serializer = ProductImageSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = PaikarSaleOrder
        fields = (
            "product",
            "company",
            "product_grade",
            "has_vat",
            "vat_ratio",
            "orderlines",
            "validity_dates",
            "ecomm_identifier",
            "reviews",
            "images",
        )
