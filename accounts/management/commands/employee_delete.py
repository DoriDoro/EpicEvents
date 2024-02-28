import sys

from django.core.management import call_command

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import create_model_table, create_pretty_table


class Command(EpicEventsCommand):
    """
    This class `Command` is a subclass of `EpicEventsCommand` designed for managing employee
    deletions within a system. It is specifically tailored for users with "MA" permissions,
    indicating that it is intended for managers.

    - `help`: A string describing the command's purpose, which is to prompt for details necessary
        to delete an employee.
    - `action`: A string indicating the action associated with this command, set to "DELETE".
    - `permissions`: A list of roles that are allowed to execute this command, in this case, only
        "MA" (Management) has the permission.

    Key methods within this class include:

    - `get_create_model_table`: Generates a table of all employees emails to help the user select
        an employee to delete.
    - `get_requested_model`: Prompts the user to input the email address of the employee they wish
        to delete and displays the employee's details for confirmation.
    - `get_data`: Prompts the user to confirm the deletion of the selected employee.
    - `make_changes`: If the user confirms the deletion, it proceeds to delete the employee;
        otherwise, it cancels the operation and returns to the employee management interface.
    - `collect_changes`: Confirms the deletion of the employee and displays a success message.
    - `go_back`: Provides an option to go back to the previous command, presumably to the main
        employee management interface.

    This class encapsulates the functionality for deleting employees, ensuring that only users with
    the appropriate permissions can perform this action. It leverages
    the `EpicEventsCommand` class for common command functionalities, such as displaying input
    prompts and handling user input.
    """

    help = "Delete an employee."
    action = "DELETE"
    permissions = ["MA"]

    def get_create_model_table(self):
        create_model_table(Employee, "user.email", "Employee Emails")

    def get_requested_model(self):
        while True:
            self.display_input_title("Enter details:")

            email = self.email_input("Email address")
            self.object = Employee.objects.filter(user__email=email).first()

            if self.object:
                break
            else:
                create_invalid_error_message("email")

        self.stdout.write()
        employee_table = [
            ["Email: ", self.object.user.email],
            ["First name: ", self.object.first_name],
            ["Last name: ", self.object.last_name],
            ["Role: ", self.object.get_role_display()],
        ]
        create_pretty_table(employee_table, "Details of the Employee: ")

    def get_data(self):
        self.display_input_title("Enter choice:")

        return {
            "delete": self.choice_str_input(
                ("Y", "N"), "Choice to delete [Y]es or [N]o"
            ),
        }

    def make_changes(self, data):
        if data["delete"] == "Y":
            self.object.user.delete()
        if data["delete"] == "N":
            self.stdout.write()
            call_command("employee")
            sys.exit()

    def collect_changes(self):
        create_success_message("Employee", "deleted")

    def go_back(self):
        call_command("employee")
