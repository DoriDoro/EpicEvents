from django.contrib.auth import get_user_model
from django.core.management import call_command

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import (
    create_model_table,
    create_pretty_table,
)

UserModel = get_user_model()


class Command(EpicEventsCommand):
    help = "Prompts for details to to update a client."
    action = "UPDATE"

    def get_create_model_table(self):
        create_model_table(Client, "email", "Client Emails")

    def get_requested_model(self):
        while True:
            email = self.email_input("Email address")
            self.object = Client.objects.filter(email=email).first()

            if self.object:
                break
            else:
                create_invalid_error_message("email")

        self.stdout.write()
        client_table = [
            ["[E]mail: ", self.object.email],
            ["[F]irst name: ", self.object.first_name],
            ["[L]ast name: ", self.object.last_name],
            ["[P]hone: ", self.object.phone],
            ["[C]ompany name: ", self.object.company_name],
        ]
        create_pretty_table(client_table, "Details of the Client: ")

    def get_fields_to_update(self):
        self.fields_to_update = self.multiple_choice_str_input(
            ("E", "F", "L", "P", "C"), "Your choice? [E, F, L, P, C]"
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
            "P": {
                "method": self.int_input,
                "params": {"label": "Phone"},
                "label": "phone",
            },
            "C": {
                "method": self.text_input,
                "params": {"label": "Company name"},
                "label": "company_name",
            },
        }
        return self.available_fields

    def get_data(self):
        self.update_fields = list()
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

    def make_changes(self, data):
        Client.objects.filter(email=self.object.email).update(**data)

        self.object.refresh_from_db()

        return self.object

    def display_changes(self):
        # overwrite self.update_fields to display all fields
        self.update_fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "company_name",
        ]
        create_success_message("Client", "updated")
        super().display_changes()

    def go_back(self):
        call_command("client")
