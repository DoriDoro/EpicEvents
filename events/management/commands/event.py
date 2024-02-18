from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_app_menu


class Command(EpicEventsCommand):
    help = "Menu for all operations around the events."
    permissions = ["SA", "SU", "MA"]

    def handle(self, *args, **options):
        super().handle(*args, **options)

        choice = get_app_menu("event")

        if choice == 1:
            call_command("event_list_filter")
        if choice == 2:
            call_command("event_create")
        if choice == 3:
            call_command("event_update")
        if choice == 4:
            call_command("event_delete")
        if choice == 5:
            call_command("event_filter")
        if choice == 6:
            call_command("start")
