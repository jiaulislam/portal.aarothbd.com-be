import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from faker import Faker

from apps.company.models import Company

fake = Faker()


class CompanyFactory(DjangoModelFactory):
    name = factory.LazyFunction(fake.company)
    bin_number = factory.LazyFunction(fake.bban)
    tin_number = factory.LazyFunction(fake.aba)

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)

    class Meta:
        model = Company
