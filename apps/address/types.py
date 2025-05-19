from typing import NotRequired

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.types import BaseSerializerValidatedDataType


class AddressType(models.TextChoices):
    DEFAULT = "default", _("Default Address")
    DELIVERY = "delivery", _("Delivery Address")
    CONTACT = "contact", _("Contact Address")
    GENERAL = "general", _("General Address")
    SHIPPING = "shipping", _("Shipping Address")
    BILLING = "billing", _("Billing Address")


class AddressValidatedDataType(BaseSerializerValidatedDataType):
    line_1: NotRequired[str]
    line_2: NotRequired[str]
    sub_district: int | models.Model
    district: int | models.Model
    division: int | models.Model
    country: int | models.Model
    address_type: AddressType
