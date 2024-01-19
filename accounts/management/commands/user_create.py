from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Command to create a new user."

    def add_arguments(self, parser):
        parser.add_argument(
            "email", type=str, help="Email address to create a new user."
        )
        parser.add_argument("password", type=str, help="Password to create a new user.")

    def handle(self, *args, **options):
        UserModel.objects.create_user(
            email=options["email"], password=options["password"]
        )
