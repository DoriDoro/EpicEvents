from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_error_message, create_success_message
from cli.utils_tables import create_model_table

UserModel = get_user_model()


class Command(EpicEventsCommand):
    help = "Prompts for details to create a new client."
    action = "CREATE"

    def get_create_model_table(self):
        create_model_table(Client, "email", "Client Emails")

    def get_data(self):
        return {
            "email": self.email_input("Email address"),
            "first_name": self.text_input("First name"),
            "last_name": self.text_input("Last name"),
            "phone": self.int_input("Phone number"),
            "company_name": self.text_input("Company name"),
        }

    def make_changes(self, data):
        try:
            self.object = Client.objects.create(**data)
        except IntegrityError:
            create_error_message("Email")
            call_command("client_create")

    def display_changes(self):
        self.update_fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "company_name",
        ]
        self.update_table = []
        create_success_message("Client", "created")
        super().display_changes()

    def go_back(self):
        call_command("client")
