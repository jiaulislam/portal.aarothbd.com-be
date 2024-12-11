import sys

from devtools import debug
from django.core import management
from django.core.management import BaseCommand, base
from sentry_sdk import capture_exception


class Command(BaseCommand):
    help = "Load all the constant objects by running other load commands"

    def add_arguments(self, parser: base.CommandParser):
        parser.add_argument("--test_company", type=bool, default=None)

    def handle(self, *args, **options):
        sys.stdout.write("Loading constants Started\n")
        try:
            sys.stdout.write("Creating superuser with default data started\n")
            self.create_default_superuser()
            sys.stdout.write("Creating superuser with default data finished\n")

            sys.stdout.write("Loading Country started\n")
            management.call_command("load_countries")
            sys.stdout.write("Loading Country finished\n")

            sys.stdout.write("Loading BD Division started\n")
            management.call_command("load_bd_divisions")
            sys.stdout.write("Loading BD Divisions finished\n")

            sys.stdout.write("Loading BD Districts started\n")
            management.call_command("load_bd_districts")
            sys.stdout.write("Loading BD Districts finished\n")

            sys.stdout.write("Loading BD Sub-Districts started\n")
            management.call_command("load_bd_sub_districts")
            sys.stdout.write("Loading BD Sub-Districts finished\n")

            if options.get("test_company"):
                sys.stdout.write("Loading BD Sub-Districts started\n")
                management.call_command("load_demo_companies")
                sys.stdout.write("Loading BD Sub-Districts finished\n")
        except Exception as exc:
            debug(exc)
            capture_exception(exc)
        return

    def create_default_superuser(self):
        from django.contrib.auth import get_user_model

        User = get_user_model() # noqa: N806
        email = "superadmin@aarothbd.com"
        password = "Admin@123"

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            sys.stdout.write(f"Superuser created: {email}\n")
        else:
            raise Exception(f"User {email} already exists!")
