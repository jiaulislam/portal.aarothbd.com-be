import json
import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.sub_district.models import SubDistrict
from core.settings.django.base import BASE_DIR


class Command(BaseCommand):
    help = "Load Sub Districts for Bangladesh"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            sub_district_file = BASE_DIR / "apps/data_migration/data/bd_sub_districts.json"
            sub_district_instances = []
            with open(sub_district_file) as json_file:
                sub_districts = json.load(json_file)
                for sub_district in sub_districts:
                    instance = SubDistrict(
                        id=sub_district.get("id"),
                        name=sub_district.get("name"),
                        bn_name=sub_district.get("bn_name"),
                        district_id=sub_district.get("district_id"),
                        created_by_id=sub_district.get("created_by_id"),
                        updated_by_id=sub_district.get("updated_by_id"),
                    )
                    sub_district_instances.append(instance)
                sub_districts = SubDistrict.objects.bulk_create(sub_district_instances)
                sys.stdout.write(f"{len(sub_districts)} Sub Districts loaded\n")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found !"))
