import sys

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError, transaction

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_error_message, create_success_message
from cli.utils_tables import create_queryset_table

UserModel = get_user_model()


class Command(EpicEventsCommand):
    """
    This class `Command` is a subclass of `EpicEventsCommand` designed to facilitate the creation
    of new employees within a system. It is specifically tailored for users with "MA" permissions,
    indicating that it is intended for management.

    - `help`: A string describing the command's purpose, which is to prompt for details necessary
        to create a new employee.
    - `action`: A string indicating the action associated with this command, set to "CREATE".
    - `permissions`: A list of roles that are allowed to execute this command, in this case, only
        "MA" (Management) has the permission.

    Key methods within this class include:

    - `get_queryset`: Initializes the queryset for `Employee` objects, selecting related `User`
        objects for each employee.
    - `get_create_model_table`: Generates tables of all employees and a subset of employees
        related to the current user, displaying relevant information such as email, first name,
        last name and role.
    - `get_data`: Prompts the user to input details for creating a new employee, capturing email,
        password, first name, last name and role.
    - `make_changes`: Attempts to create a new `User` and a new `Employee` object with the
        provided data. Handles potential `IntegrityError` by displaying an error message and
        re-prompting the user to create an employee.
    - `collect_changes`: Confirms the creation of a new employee and displays a success message.
    - `go_back`: Provides an option to go back to the previous command, presumably to the main
        employee management interface.

    This class encapsulates the functionality for creating new employees, ensuring that only users
    with the appropriate permissions can perform this action. It leverages the `EpicEventsCommand`
    class for common command functionalities, such as displaying input prompts
    and handling user input.
    """

    help = "Prompts to create a new employee."
    action = "CREATE"
    permissions = ["MA"]

    def get_queryset(self):
        self.queryset = (
            Employee.objects.select_related("user").only("user__email").all()
        )

    def get_instance_data(self):
        super().get_instance_data()
        table_data = dict()

        for employee in self.queryset:
            employee_data = {
                "email": employee.user.email,
                "name": employee.get_full_name,
                "role": employee.role,
            }
            table_data[f"Employee {employee.id}"] = employee_data

        create_queryset_table(table_data, "Employee", headers=self.headers["employee"])

    def get_data(self):
        self.display_input_title("Enter details to create an employee:")

        return {
            "email": self.email_input("Email address"),
            "password": self.password_input("Password"),
            "first_name": self.text_input("First name"),
            "last_name": self.text_input("Last name"),
            "role": self.choice_str_input(
                ("SA", "SU", "MA"), "Role [SA]les, [SU]pport, [MA]nagement"
            ),
        }

    @transaction.atomic
    def make_changes(self, data):
        try:
            user = UserModel.objects.create_user(
                data.pop("email", None), data.pop("password", None)
            )
            self.object = Employee.objects.create(**data, user=user)
            return self.object

        except IntegrityError:
            create_error_message("Email")
            call_command("employee_create")
            sys.exit()

    def collect_changes(self):
        self.fields = ["email", "first_name", "last_name", "role"]

        create_success_message("Employee", "created")
        self.update_table.append([f"Email: ", self.object.user.email])
        super().collect_changes()

    def go_back(self):
        call_command("employee")
        sys.exit()
