from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cli.menu import get_app_menu

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Menu for all operations around the account managers."

    def handle(self, *args, **options):
        choice = get_app_menu("employee")

        if choice == 4:
            call_command("start")
        if choice == 1:
            call_command("employee_create")
