from django.core.management import call_command

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_model_table


class Command(EpicEventsCommand):
    help = "Lists all clients."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        # TODO: more details of the client [employee, email, first_name, etc]
        create_model_table(Client, "email", "Client Emails")

    def go_back(self):
        call_command("client")
