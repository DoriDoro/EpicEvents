from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_start_menu
from cli.utils_messages import create_info_message


class Command(EpicEventsCommand):
    help = "Start of the program."
    permissions = ["SA", "SU", "MA"]

    def handle(self, *args, **options):
        super().handle(*args, **options)

        choice = get_start_menu("Epic Events")

        if choice == 1:
            call_command("employee")
        if choice == 2:
            call_command("client")
        if choice == 3:
            call_command("contract")
        if choice == 4:
            call_command("event")
        if choice == 5:
            return
        if choice == 6:
            self.logout()
            create_info_message("Logging out...")
            return
