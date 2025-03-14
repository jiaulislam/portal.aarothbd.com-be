from django.core.management.base import BaseCommand
from django.db import transaction

from apps.user.models import User


class Command(BaseCommand):
    help = "Fill username with email or phone"

    @transaction.atomic
    def handle(self, *args, **options):
        users = User.objects.filter(user_name__isnull=True)
        for user in users:
            user.user_name = user.email or user.phone
        User.objects.bulk_update(users, ["user_name"])
