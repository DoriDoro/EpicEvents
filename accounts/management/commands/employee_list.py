from django.core.management import call_command

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_model_table


class Command(EpicEventsCommand):
    help = "Lists all employees."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        # TODO: more details of the employee [email, role]
        # TODO: column_label as *arg and as parameter a list of column_labels ['email', 'role']
        create_model_table(Employee, "user.email", "Employee Emails")

    def go_back(self):
        call_command("employee")
