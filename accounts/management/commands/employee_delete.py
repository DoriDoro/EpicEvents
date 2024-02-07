from django.core.management import call_command

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import create_model_table, create_pretty_table


class Command(EpicEventsCommand):
    help = "Delete an employee."
    action = "DELETE"

    def get_create_model_table(self):
        create_model_table(Employee, "user.email", "Employee Emails")

    def get_requested_model(self):
        while True:
            email = self.email_input("Email address")
            self.object = Employee.objects.filter(user__email=email).first()

            if self.object:
                break
            else:
                create_invalid_error_message("email")

        self.stdout.write()

        role_value = self.check_role_value()

        employee_table = [
            ["Email: ", self.object.user.email],
            ["First name: ", self.object.first_name],
            ["Last name: ", self.object.last_name],
            ["Role: ", role_value],
        ]
        create_pretty_table(employee_table, "Details of the Employee: ")

    def get_data(self):
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

    def display_changes(self):
        create_success_message("Employee", "deleted")

    def go_back(self):
        call_command("employee")
