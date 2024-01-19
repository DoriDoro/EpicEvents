from django.core.management import call_command
from django.core.management.base import BaseCommand

from cli.menu import get_app_menu


class Command(BaseCommand):
    help = "Menu for all operations around the users."

    def handle(self, *args, **options):
        choice = get_app_menu("user")

        if choice == 1:
            call_command("user_input_create")
        if choice == 2:
            call_command("user_input_update")
        if choice == 3:
            call_command("user_delete")
        if choice == 4:
            call_command("start")
