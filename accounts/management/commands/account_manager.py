from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cli.menu import get_app_menu

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Menu for all operations around the account managers."

    def handle(self, *args, **options):
        choice = get_app_menu("account manager")

        if choice == 4:
            call_command("start")
        if choice == 1:
            email = str(
                input("Please enter the email address of the future account manager: ")
            )  # search for the email address of user
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                print(
                    "This email address is not known. Please enter a valid email address."
                )  # improve this logic, implement while loop
            f_name = str(input("Please enter the first name: "))
            l_name = str(input("Please enter the last name: "))
            role = str(
                input("Please enter the role: ")
            )  # improve to make a choice between possible roles

            call_command(
                "account_manager_create",
                user.id,
                f_name,
                l_name,
                role,
            )  # when token is in place user will be different
