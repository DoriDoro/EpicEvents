from django.core.management import call_command

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import create_model_table, create_pretty_table


class Command(EpicEventsCommand):
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

    def collect_changes(self):
        create_success_message("Employee", "deleted")

    def go_back(self):
        call_command("employee")
