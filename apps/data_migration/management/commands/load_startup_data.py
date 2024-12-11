import sys

from django.contrib.auth import get_user_model
from django.core import management
from django.core.management import BaseCommand, base

from core.settings.django.base import env

User = get_user_model()  # noqa: N806


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

            sys.stdout.write("Creating Admin with default data started\n")
            self.create_default_central_admin_user()
            sys.stdout.write("Creating Admin with default data finished\n")

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
                sys.stdout.write("Loading Test Companies started\n")
                management.call_command("load_demo_companies")
                sys.stdout.write("Loading Test Companies finished\n")
        except Exception as exc:
            raise Exception(exc)
        return

    def create_default_central_admin_user(self):
        email = env("ADMIN_USER_EMAIL")
        password = env("ADMIN_USER_PASS")

        if not User.objects.filter(email=email).exists():
            User.objects.create_user(email=email, password=password, is_admin=True, user_type="central_admin")
            sys.stdout.write(f"Admin User created: {email}\n")
        else:
            raise Exception(f"User {email} already exists!")

    def create_default_superuser(self):
        email = env("SUPER_USER_EMAIL")
        password = env("SUPER_USER_PASS")

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            sys.stdout.write(f"Superuser created: {email}\n")
        else:
            raise Exception(f"User {email} already exists!")
