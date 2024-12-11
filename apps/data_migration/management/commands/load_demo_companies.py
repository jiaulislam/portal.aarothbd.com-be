from django.core.management import BaseCommand

from apps.company.tests.company_factory import CompanyFactory
from core.services import capture_exception_sentry


class Command(BaseCommand):
    help = "Load Demo Companies"
    max_instance = 500

    def handle(self, *args, **options):
        try:
            companies = CompanyFactory.create_batch(self.max_instance)
            return len(companies)
        except Exception as e:
            capture_exception_sentry(e)
            return
