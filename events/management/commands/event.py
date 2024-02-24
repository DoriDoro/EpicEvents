from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_app_menu


class Command(EpicEventsCommand):
    """
    This script defines a class `Command` that inherits from `EpicEventsCommand`. It provides a
    menu for operations around events based on the user's role.

    - The `help` attribute provides a brief description of the command's purpose.
    - The `permissions` attribute lists the roles that have permission to execute this command.
    - The `handle` method is overridden to customize the command's behavior based on the user's
        role and their choice from the application menu.

    The `handle` method performs the following operations:
    - Calls the superclass's `handle` method to ensure proper initialization.
    - Retrieves the user's choice from the application menu for the "event" section.
    - Depending on the user's role (`SA`, `SU`, or `MA`), it executes different commands based
        on the user's choice:
        - For `SA` role:
            - Choice  1: Calls `event_list_filter` command.
            - Choice  2: Calls `event_create` command.
            - Choice  3: Calls `start` command.
        - For `SU` and `MA` role:
            - Choice  1: Calls `event_list_filter` command.
            - Choice  2: Calls `event_update` command.
            - Choice  3: Calls `start` command.

    This class demonstrates the use of inheritance and role-based access control in a command-line
    interface, allowing for a flexible and secure management of event operations.
    """

    help = "Menu for all operations around the events."
    permissions = ["SA", "SU", "MA"]

    def handle(self, *args, **options):
        super().handle(*args, **options)

        choice = get_app_menu("event", self.user)

        if self.user.employee_users.role == "SA":
            if choice == 1:
                call_command("event_list_filter")
            if choice == 2:
                call_command("event_create")
            if choice == 3:
                call_command("start")

        if self.user.employee_users.role == "SU":
            if choice == 1:
                call_command("event_list_filter")
            if choice == 2:
                call_command("event_update")
            if choice == 3:
                call_command("start")

        if self.user.employee_users.role == "MA":
            if choice == 1:
                call_command("event_list_filter")
            if choice == 2:
                call_command("event_update")
            if choice == 3:
                call_command("start")
