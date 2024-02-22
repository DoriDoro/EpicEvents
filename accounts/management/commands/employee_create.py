from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_error_message, create_success_message
from cli.utils_tables import create_queryset_table

UserModel = get_user_model()


class Command(EpicEventsCommand):
    help = "Prompts to create a new employee."
    action = "CREATE"
    permissions = ["MA"]

    def get_queryset(self):
        self.queryset = Employee.objects.select_related("user").all()

    def get_create_model_table(self):
        table_data = dict()

        headers = [
            "",
            "** Employee email **",
            "First name",
            "Last name",
            "Role",
        ]

        for employee in self.queryset:
            employee_data = {
                "email": employee.user.email,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "role": employee.role,
            }
            table_data[f"Employee {employee.id}"] = employee_data

        create_queryset_table(table_data, "Employee", headers=headers)

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

    def collect_changes(self):
        self.fields = ["email", "first_name", "last_name", "role"]

        create_success_message("Employee", "created")
        self.update_table.append([f"Email: ", self.object.user.email])
        super().collect_changes()

    def go_back(self):
        call_command("employee")
