from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import transaction, IntegrityError

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import (
    create_success_message,
    create_invalid_error_message,
    create_error_message,
)
from cli.utils_tables import (
    create_model_table,
    create_pretty_table,
)

UserModel = get_user_model()


class Command(EpicEventsCommand):
    help = "Prompts to update an employee."
    action = "UPDATE"
    permissions = ["MA"]

    update_fields = list()
    update_table = list()

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
            ["[E]mail: ", self.object.user.email],
            ["[F]irst name: ", self.object.first_name],
            ["[L]ast name: ", self.object.last_name],
            ["[R]ole: ", self.object.get_role_display()],
        ]
        create_pretty_table(employee_table, "Details of the Employee: ")

    def get_fields_to_update(self):
        self.display_input_title("Enter choice:")

        self.fields_to_update = self.multiple_choice_str_input(
            ("E", "F", "L", "R"), "Your choice? [E, F, L, R]"
        )

    def get_available_fields(self):
        self.available_fields = {
            "E": {
                "method": self.email_input,
                "params": {"label": "Email"},
                "label": "email",
            },
            "F": {
                "method": self.text_input,
                "params": {"label": "First name"},
                "label": "first_name",
            },
            "L": {
                "method": self.text_input,
                "params": {"label": "Last name"},
                "label": "last_name",
            },
            "R": {
                "method": self.choice_str_input,
                "params": {
                    "options": ("SA", "SU", "MA"),
                    "label": "Role: [SA]les, [SU]pport or [MA]nagement",
                },
                "label": "role",
            },
        }
        return self.available_fields

    def get_data(self):
        data = dict()
        for letter in self.fields_to_update:
            if self.available_fields[letter]:
                field_data = self.available_fields.get(letter)
                method = field_data["method"]
                params = field_data["params"]
                label = field_data["label"]

                data[label] = method(**params)
                self.update_fields.append(label)

        return data

    @transaction.atomic
    # if the user.email is saved and the Employee update is not working,
    # the user.email will stay saved but the Employee update will fail
    # with transaction.atomic both will be canceled
    def make_changes(self, data):
        email = data.pop("email", None)

        if email:
            if UserModel.objects.filter(email=email).exists():
                create_error_message("This email")
                call_command("employee_update")
            else:
                user = self.object.user
                user.email = email
                user.save()

        Employee.objects.filter(user=self.object.user).update(**data)

        # Refresh the object from the database
        self.object.refresh_from_db()

        return self.object

    def display_changes(self):
        # overwrite self.update_fields to display all fields
        self.update_fields = ["email", "first_name", "last_name", "role"]

        create_success_message("Employee", "updated")

        self.update_table.append([f"Email: ", self.object.user.email])
        super().display_changes()

    def go_back(self):
        call_command("employee")
