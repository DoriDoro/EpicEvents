from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_error_message, create_success_message
from cli.utils_tables import (
    create_model_table,
    create_pretty_table,
)

UserModel = get_user_model()


class Command(EpicEventsCommand):
    help = "Prompts to update an employee."
    action = "UPDATE"

    def get_available_fields(self):
        self.available_fields = {
            "E": {
                "method": self.email_input,
                "params": {"label": "Email"},
                "label": "user__email",
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
                "params": {"options": ("SA", "SU", "MA"), "label": "Role [SA, SU, MA]"},
                "label": "role",
            },
        }
        return self.available_fields

    def get_create_model_table(self):
        create_model_table(Employee, "user.email", "Employees")

    def get_requested_model(self):
        email = self.email_input("Email address")
        self.stdout.write()
        self.object = Employee.objects.filter(user__email=email).first()

        employee_table = [
            ["[E]mail: ", self.object.user.email],
            ["[F]irst name: ", self.object.first_name],
            ["[L]ast name: ", self.object.last_name],
            ["[R]ole: ", self.object.role],
        ]
        create_pretty_table(employee_table, "Details of the Employee: ")

    def get_fields_to_update(self):
        self.fields_to_update = self.multiple_choice_str_input(
            ("E", "F", "L", "R"), " Your choice? [E, F, L, R]"
        )

    def get_data(self):
        self.update_fields = list()
        data = dict()
        # TODO: if no letter go back to Menu
        for letter in self.fields_to_update:
            if self.available_fields[letter]:
                field_data = self.available_fields.get(letter)
                method = field_data["method"]
                params = field_data["params"]
                label = field_data["label"]

                data[label] = method(**params)
                self.update_fields.append(label)

        return data

        # method, params, label = self.available_fields.get(letter)
        # data[label] = method(**params)
        # update_fields.append(label)
        # return data

    def make_changes(self, data):
        email = data.pop("user__email", None)
        if email:
            user = self.object.user
            user.email = email
            user.save()

        Employee.objects.filter(user=self.object.user).update(**data)
