from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_start_menu
from cli.utils_messages import create_info_message


class Command(EpicEventsCommand):
    """
    This script defines a class `Command` that inherits from `EpicEventsCommand`. It provides the
    start menu for choosing which model to go to next.

    - The `help` attribute provides a brief description of the command's purpose.
    - The `permissions` attribute lists the roles that have permission to execute this command.
    - The `handle` method is overridden to customize the command's behavior based on the user's
        role and their choice from the application menu.

    The `handle` method performs the following operations:
    - Calls the superclass's `handle` method to ensure proper initialization.
    - Retrieves the user's choice from the application start menu for the next step.

    This class demonstrates the use of inheritance and role-based access control in a command-line
    interface, allowing for a flexible and secure management.
    """

    help = "Start the Epic Events program."
    permissions = ["SA", "SU", "MA"]

    def handle(self, *args, **options):
        """
        Handle the command execution.

        Displays the start menu and handles user input to navigate to different sections
        of the Epic Events program.
        """
        super().handle(*args, **options)

        choice = get_start_menu("Epic Events")

        if choice == 1:
            call_command("employee")
        elif choice == 2:
            call_command("client")
        elif choice == 3:
            call_command("contract")
        elif choice == 4:
            call_command("event")
        elif choice == 5:
            return
        elif choice == 6:
            self.logout()
            create_info_message("Logging out...")
            return
