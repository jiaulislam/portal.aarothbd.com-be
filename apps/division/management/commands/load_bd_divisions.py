import json
import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.division.models import Division
from core.settings.django.base import BASE_DIR


class Command(BaseCommand):
    help = "Load Divisions for Bangladesh"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            division_file = BASE_DIR / "apps/division/data/bd_divisions.json"
            division_instances = []
            with open(division_file) as json_file:
                divisions = json.load(json_file)
                for division in divisions:
                    instance = Division(
                        id=division["id"],
                        name=division["name"],
                        bn_name=division["bn_name"],
                        lat=division["lat"],
                        long=division["long"],
                        country_id=division["country_id"],
                    )
                    division_instances.append(instance)
                divisions = Division.objects.bulk_create(division_instances)
                sys.stdout.write(f"{len(divisions)} Divisions loaded\n")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found !"))
