from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_app_menu


class Command(EpicEventsCommand):
    """
    This script defines a class `Command` that inherits from `EpicEventsCommand`. It provides a
    menu for operations around clients based on the user's role.

    - The `help` attribute provides a brief description of the command's purpose.
    - The `permissions` attribute lists the roles that have permission to execute this command.
    - The `handle` method is overridden to customize the command's behavior based on the user's
        role and their choice from the application menu.

    The `handle` method performs the following operations:
    - Calls the superclass's `handle` method to ensure proper initialization.
    - Retrieves the user's choice from the application menu for the "client" section.
    - Depending on the user's role (`SA`, `SU`, or `MA`), it executes different commands based
        on the user's choice:
        - For `SA` role:
            - Choice  1: Calls `client_list_filter` command.
            - Choice  2: Calls `client_create` command.
            - Choice  3: Calls `client_update` command.
            - Choice  4: Calls `start` command.
        - For `SU` roles:
            - Choice  1: Calls `client_list_filter` command.
            - Choice  2: Calls `start` command.
        - For `MA` roles:
            - Choice  1: Calls `client_list_filter` command.
            - Choice  2: Calls `client_delete` command.
            - Choice  3: Calls `start` command.

    This class demonstrates the use of inheritance and role-based access control in a command-line
    interface, allowing for a flexible and secure management of client operations.
    """

    help = "Menu for all operations around the clients."
    permissions = ["SA", "SU", "MA"]

    def handle(self, *args, **options):
        super().handle(*args, **options)

        choice = get_app_menu("client", self.user)

        if self.user.employee_users.role == "SA":
            if choice == 1:
                call_command("client_list_filter")
            elif choice == 2:
                call_command("client_create")
            elif choice == 3:
                call_command("client_update")
            elif choice == 4:
                call_command("start")

        if self.user.employee_users.role == "SU":
            if choice == 1:
                call_command("client_list_filter")
            elif choice == 2:
                call_command("start")

        if self.user.employee_users.role == "MA":
            if choice == 1:
                call_command("client_list_filter")
            elif choice == 2:
                call_command("client_delete")
            elif choice == 3:
                call_command("start")
