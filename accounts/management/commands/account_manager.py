from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cli.menu import get_app_menu

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Menu for all operations around the account managers."

    def handle(self, *args, **options):
        choice = get_app_menu("account manager")

        all_users = UserModel.objects.all()

        if choice == 4:
            call_command("start")
        if choice == 1:
            call_command(
                "account_manager_create",
                user=all_users[1],
                first_name="John",
                last_name="Doe",
                role="Management",
            )  # when token is in place user will be different
