from django.core.management import call_command
from django.core.management.base import BaseCommand

from cli.utils_menu import get_app_menu


class Command(BaseCommand):
    help = "Menu for all operations around the contracts."

    def handle(self, *args, **options):
        choice = get_app_menu("contract")

        if choice == 1:
            call_command("contract_create")
        if choice == 2:
            call_command("contract_update")
        if choice == 3:
            call_command("contract_delete")
        if choice == 4:
            call_command("start")
