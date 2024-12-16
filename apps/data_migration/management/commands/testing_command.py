import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test Command"

    def handle(self, *args, **options):
        sys.stdout.write("Testing Success\n")
