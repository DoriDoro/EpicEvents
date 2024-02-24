from django.core.management import call_command

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_queryset_table


class Command(EpicEventsCommand):
    """
    This class `Command` is a subclass of `EpicEventsCommand` designed to list all employees
    within the system. It is accessible to users with "SA" (Sales), "SU" (Support),
    or "MA" (Management) permissions.

    - `help`: A string describing the command's purpose, which is to list all employees.
    - `action`: A string indicating the action associated with this command, set to "LIST".
    - `permissions`: A list of roles that are allowed to execute this command.

    Key methods within this class include:

    - `get_queryset`: Initializes the queryset for `Employee` objects, selecting related `User`
        objects for each employee.
    - `get_create_model_table`: Generates a table of all employees, displaying relevant
        information such as email, full name, and role.
    - `go_back`: Provides an option to go back to the previous command, presumably to the main
        employee management interface.

    This class encapsulates the functionality for listing all employees, ensuring that only users
    with the appropriate permissions can perform this action. It leverages the `EpicEventsCommand`
    class for common command functionalities, such as displaying input prompts
    and handling user input.
    """

    help = "Lists all employees."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_queryset(self):
        self.queryset = Employee.objects.select_related("user").all()

    def get_create_model_table(self):
        table_data = dict()

        headers = ["", "** Employee email **" "", "Name", "Role"]

        for employee in self.queryset:
            employee_data = {
                "email": employee.user.email,
                "name": employee.get_full_name,
                "role": employee.role,
            }
            table_data[f"Employee {employee.id}"] = employee_data

        create_queryset_table(table_data, "Employees", headers=headers)

    def go_back(self):
        call_command("employee")
