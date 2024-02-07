from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates a superuser."

    def handle(self, *args, **options):
        try:
            UserModel.objects.create_superuser("admin", "admin@mail.com", "admin")
        except IntegrityError:
            self.stdout.write(self.style.WARNING("Exists already!"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser successfully created!"))
