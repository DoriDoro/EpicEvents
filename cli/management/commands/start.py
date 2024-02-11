from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_start_menu


class Command(EpicEventsCommand):
    help = "Start of the program."

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
        if choice == 6:
            self.logout()
            self.stdout.write(" Logging out...")
            return
