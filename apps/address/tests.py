from factory.django import DjangoModelFactory

from .models import Address


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address
