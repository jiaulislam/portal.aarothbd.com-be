from django.core import management
from django.core.management import BaseCommand, base
from sentry_sdk import capture_exception


class Command(BaseCommand):
    help = "Execute Custom Script"

    def add_arguments(self, parser: base.CommandParser):
        parser.add_argument("command_name")

    def handle(self, *args, **options):
        try:
            command_name = options.get("command_name", "")
            if bool(command_name):
                raise ValueError("Empty command not allowed !")
            management.call_command(command_name)
        except Exception as exc:
            capture_exception(exc)
        return
