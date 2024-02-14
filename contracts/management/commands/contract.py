from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_app_menu


class Command(EpicEventsCommand):
    help = "Menu for all operations around the contracts."
    permissions = ["SA", "SU", "MA"]

    def handle(self, *args, **options):
        super().handle(*args, **options)

        choice = get_app_menu("contract")

        if choice == 1:
            call_command("contract_list")
        if choice == 2:
            call_command("contract_create")
        if choice == 3:
            call_command("contract_update")
        if choice == 4:
            call_command("contract_delete")
        if choice == 5:
            call_command("start")
