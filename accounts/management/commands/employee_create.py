from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_error_message, create_success_message
from cli.utils_tables import create_model_table

UserModel = get_user_model()


class Command(EpicEventsCommand):
    help = "Prompts to create a new employee."
    action = "CREATE"

    def get_create_model_table(self):
        create_model_table(Employee, "user.email", "Employee Emails")

    def get_data(self):
        return {
            "email": self.email_input("Email address"),
            "password": self.password_input("Password"),
            "first_name": self.text_input("First name"),
            "last_name": self.text_input("Last name"),
            "role": self.choice_str_input(("SA", "SU", "MA"), "Role [SA, SU, MA]"),
        }

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

    def display_changes(self):
        self.update_fields = ["email", "first_name", "last_name", "role"]
        create_success_message("Employee", "created")
        super().display_changes()
        self.update_table.append([f"Email: ", self.object.user.email])

    def go_back(self):
        call_command("employee")
