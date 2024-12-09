from django.core.management import BaseCommand, base

from apps.company.tests.company_factory import CompanyFactory
from core.services import capture_exception_sentry


class Command(BaseCommand):
    help = "Load Demo Companies"
    max_instance = 500

    def add_arguments(self, parser: base.CommandParser):
        parser.add_argument("--quantity", type=int, help="Number of test companies to load")

    def handle(self, *args, **options):
        try:
            quantity = options.get("quantity", self.max_instance)
            companies = CompanyFactory.create_batch(quantity)
            return len(companies)
        except Exception as e:
            capture_exception_sentry(e)
            return
