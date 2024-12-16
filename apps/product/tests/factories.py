import string
from random import choice

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from apps.country.models import Country
from apps.uom.models import UoM

from ..models.product_brand_model import ProductBrand
from ..models.product_category_model import ProductCategory
from ..models.product_model import Product, ProductDetail

PARENT_CATEGORIS = [
    "Electronics",
    "Books",
    "Clothing",
    "Home Appliances",
    "Furniture",
    "Toys",
    "Groceries",
    "Stationery",
]

REAL_CATEGORIES = [
    "Sports Equipment",
    "Beauty Products",
    "Automotive",
    "Health & Wellness",
    "Pet Supplies",
    "Gardening",
    "Baby Products",
    "Musical Instruments",
    "Art Supplies",
    "Office Supplies",
    "Gaming",
    "Outdoor Gear",
    "Footwear",
    "Watches",
    "Luggage",
    "Kitchenware",
    "Fitness Equipment",
    "Bicycles",
    "Board Games",
    "DIY Tools",
    "Perfumes",
    "Mobile Accessories",
    "Laptop Accessories",
    "Cameras",
    "Lighting",
    "Cleaning Supplies",
    "Party Supplies",
    "Craft Materials",
    "Seasonal Decorations",
    "Books & Stationery",
    "Personal Care",
    "Smart Home Devices",
    "Drones",
    "Camping Gear",
    "Fishing Gear",
    "Travel Essentials",
    "Handbags",
    "Cookware",
    "Organic Food",
    "Wine & Spirits",
    "Puzzles",
    "Educational Toys",
    "Skincare",
    "Hair Care",
    "Bath Accessories",
    "Sportswear",
    "Hiking Gear",
    "Sunglasses",
    "Action Figures",
    "Bedding",
    "Curtains",
    "Wallpaper",
    "Mirrors",
    "Paint Supplies",
    "Car Accessories",
    "Motorcycle Gear",
    "Safety Equipment",
    "Survival Gear",
    "Science Kits",
    "Boarding Pass Wallets",
    "Comics",
    "Luxury Goods",
    "Gift Cards",
    "Subscriptions",
    "Magazines",
    "Antiques",
    "Collectibles",
    "Fine Art",
    "Handcrafted Goods",
    "Seasonal Gifts",
    "Wedding Supplies",
    "Event Decorations",
    "Meditation Accessories",
    "Yoga Gear",
    "Electric Scooters",
    "Energy-Saving Devices",
    "Recycling Bins",
    "Water Purifiers",
    "Air Purifiers",
    "Video Games",
    "Streaming Devices",
    "Portable Speakers",
    "Headphones",
    "Virtual Reality Gear",
    "Action Cameras",
    "Smartwatches",
    "Fitness Trackers",
    "E-books",
    "Audio Books",
    "Child Safety Products",
    "Camping Tents",
    "Sleeping Bags",
]


class ProductCategoryFactory(DjangoModelFactory):
    name = factory.LazyFunction(lambda: choice(REAL_CATEGORIES))
    parent = factory.LazyFunction(lambda: choice(ProductCategory.objects.filter(parent__isnull=True)))

    class Meta:
        model = ProductCategory


class ProductBrandFactory(DjangoModelFactory):
    name = (
        factory.fuzzy.FuzzyText(
            chars=string.ascii_letters,
            prefix="B-",
            length=12,
        )
        .fuzz()
        .title()
    )

    class Meta:
        model = ProductBrand


class ProductFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Product %08d" % n)
    description = factory.Faker("sentence")
    sku_code = factory.Faker("bothify", text="SKU-####")
    uom = factory.LazyFunction(lambda: choice(UoM.objects.all()))
    category = factory.LazyFunction(lambda: choice(ProductCategory.objects.filter(parent__isnull=False)))
    has_detail = factory.LazyFunction(lambda: choice((True, False)))
    brand = factory.LazyFunction(lambda: choice([ProductBrandFactory(), None]))
    origin = factory.LazyFunction(lambda: choice(Country.objects.all()))
    html = factory.Faker("paragraph")

    class Meta:
        model = Product


class ProductDetailFactory(DjangoModelFactory):
    product = factory.LazyFunction(lambda: choice(Product.objects.filter(has_detail=True)))
    size_name = factory.Faker("word")
    size_description = factory.Faker("sentence")

    class Meta:
        model = ProductDetail

    @classmethod
    def create_instance(cls, product):
        return cls.create(product=product)
