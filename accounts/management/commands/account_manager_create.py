from django.core.management.base import BaseCommand

from accounts.models import AccountManager


class Command(BaseCommand):
    help = "Creates a new account manager."

    def add_arguments(self, parser):
        parser.add_argument("user", type=int, help="Enter the user id.")
        parser.add_argument("first_name", type=str, help="Enter the first name.")
        parser.add_argument("last_name", type=str, help="Enter the last name.")
        parser.add_argument("role", type=str, help="Enter the role.")

    def handle(self, *args, **options):
        """necessary data to create an account manager:
        - user
        - first_name
        - last_name
        - role
        """
        account_manager = AccountManager(
            user=options["user"],
            first_name=options["first_name"],
            last_name=options["last_name"],
            role=options["role"],
        )
        account_manager.save()

        print("New account manager was created.")
