import json
import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.district.models import District
from core.settings.django.base import BASE_DIR


class Command(BaseCommand):
    help = "Load Districts for Bangladesh"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            district_file = BASE_DIR / "apps/district/data/bd_districts.json"
            district_instances = []
            with open(district_file) as json_file:
                districts = json.load(json_file)
                for district in districts:
                    instance = District(
                        id=district["id"],
                        name=district["name"],
                        bn_name=district["bn_name"],
                        lat=district["lat"],
                        long=district["long"],
                        division_id=district["division_id"],
                    )
                    district_instances.append(instance)
                districts = District.objects.bulk_create(district_instances)
                sys.stdout.write(f"{len(districts)} Districts loaded\n")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found !"))
