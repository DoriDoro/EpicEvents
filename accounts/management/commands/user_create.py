from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Creates a new user."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Enter the email address.")
        parser.add_argument("password", type=str, help="Enter the password.")

    def handle(self, *args, **options):
        """necessary data to create a user:
        - email
        - password
        """

        UserModel.objects.create_user(
            email=options["email"], password=options["password"]
        )

        self.stdout.write("New user was created.")
