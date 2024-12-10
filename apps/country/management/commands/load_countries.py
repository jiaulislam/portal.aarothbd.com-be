import json
import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.country.models import Country
from core.settings.django.base import BASE_DIR


class Command(BaseCommand):
    help = 'Load Countries With Continent'

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            countries_json_file_path = BASE_DIR / "apps/country/data/countries.json"
            country_instances= []
            with open(countries_json_file_path) as json_file:
                country_maps = json.load(json_file)
                country_keys = country_maps.keys()
                for key in country_keys:
                    country = country_maps[key]
                    instance  = Country(
                        continent_code=country.get('continent_code'),
                        continent_name=country.get('continent_name'),
                        name=country.get('country_name'),
                        full_name=country.get('country_name_full'),
                        country_code=country.get('country_code2'),
                        country_code_alpha3=country.get('country_code3'),
                        country_code_iso3=country.get('iso3'),
                    )
                    country_instances.append(instance)
                countries = Country.objects.bulk_create(country_instances)
                sys.stdout.write(f"{len(countries)} Countries loaded\n")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found !"))
