from django.core.management import call_command

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_queryset_table


class Command(EpicEventsCommand):
    help = "Lists all employees."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        table_data = dict()

        queryset = Employee.objects.select_related("user").all()
        headers = ["", "email", "first name", "last name", "role"]

        for employee in queryset:
            employee_data = {
                "email": employee.user.email,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "role": employee.role,
            }
            table_data[f"Employee {employee.id}"] = employee_data

        create_queryset_table(table_data, "Test", headers=headers)

    def go_back(self):
        call_command("employee")
