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
            division_file = BASE_DIR / "apps/data_migration/data/bd_divisions.json"
            division_instances = []
            with open(division_file) as json_file:
                divisions = json.load(json_file)
                for division in divisions:
                    instance = Division(
                        id=division.get("id"),
                        name=division.get("name"),
                        bn_name=division.get("bn_name"),
                        lat=division.get("lat"),
                        long=division.get("long"),
                        country_id=division.get("country_id"),
                        created_by_id=division.get("created_by_id", 1),
                        updated_by_id=division.get("updated_by_id", 1),
                    )
                    division_instances.append(instance)
                divisions = Division.objects.bulk_create(division_instances)
                sys.stdout.write(f"{len(divisions)} Divisions loaded\n")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found !"))
