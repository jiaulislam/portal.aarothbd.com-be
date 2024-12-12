from django.db import models
from django.utils.translation import gettext_lazy as _


class AddressType(models.TextChoices):
    DEFAULT = "default", _("Default Address")
    DELIVERY = "delivery", _("Delivery Address")
    CONTACT = "contact", _("Contact Address")
    GENERAL = "general", _("General Address")
