from django.core.management import call_command
from django.db import IntegrityError

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_error_message, create_success_message
from cli.utils_tables import create_model_table


class Command(EpicEventsCommand):
    help = "Prompts for details to create a new client."
    action = "CREATE"
    permissions = ["SA"]

    def get_create_model_table(self):
        create_model_table(Client, "email", "Client Emails")

    def get_data(self):
        self.display_input_title("Enter details to create a client:")

        return {
            "email": self.email_input("Email address"),
            "first_name": self.text_input("First name"),
            "last_name": self.text_input("Last name"),
            "phone": self.int_input("Phone number"),
            "company_name": self.text_input("Company name"),
        }

    def make_changes(self, data):
        try:
            self.object = Client.objects.create(
                employee=self.user.employee_users, **data
            )
        except IntegrityError:
            create_error_message("Email")
            call_command("client_create")

    def collect_changes(self):
        self.update_fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "company_name",
        ]

        create_success_message("Client", "created")
        super().collect_changes()

    def go_back(self):
        call_command("client")
