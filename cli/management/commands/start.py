from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_menu import get_start_menu
from cli.utils_messages import create_info_message


class StartProgramCommand(EpicEventsCommand):
    """
    Command to start the Epic Events program.

    This command displays the start menu of the Epic Events program and allows users
    with appropriate permissions to navigate to different sections of the program.

    Permissions for Employees with role:
        - SA: Sales
        - SU: Support
        - MA: Management
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
