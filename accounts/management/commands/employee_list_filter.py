from django.core.management import call_command

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_queryset_table, create_pretty_table


class Command(EpicEventsCommand):
    """
    Command to list all Employees.

    This command displays all Employees with get_create_model_table, finish the command and
    goes back to the employee menu.

    Permissions for Employees with role:
        - SA: Sales
        - SU: Support
        - MA: Management
    """

    help = "Lists all employees."
    action = "LIST_FILTER"
    permissions = ["SA", "SU", "MA"]

    def get_queryset(self):
        self.queryset = Employee.objects.select_related("user").all()

    def get_create_model_table(self):
        table_data = dict()

        headers = ["", "email", "name", "role"]

        for employee in self.queryset:
            employee_data = {
                "email": employee.user.email,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "role": employee.role,
            }
            table_data[f"Employee {employee.id}"] = employee_data

        create_queryset_table(table_data, "Employees", headers=headers)

    def go_back(self):
        call_command("employee")
