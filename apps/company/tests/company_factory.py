import factory
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from faker import Faker

from apps.company.models import Company, CompanyConfiguration

fake = Faker()

User = get_user_model()

root_user = User.objects.get(pk=1)


class CompanyConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = CompanyConfiguration


class CompanyFactory(DjangoModelFactory):
    name = factory.LazyFunction(fake.company)
    bin_number = factory.LazyFunction(fake.bban)
    tin_number = factory.LazyFunction(fake.aba)
    configuration = factory.SubFactory(CompanyConfigurationFactory)
    created_by = root_user
    updated_by = root_user

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)  # type: ignore

    class Meta:
        model = Company
