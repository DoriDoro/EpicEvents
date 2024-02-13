from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_model_table
from events.models import Event


class Command(EpicEventsCommand):
    help = "Lists all events."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        # TODO: more details of the contracts [contract.client, date, name, location, max_guests]
        create_model_table(Event, "contract.client.email", "Client emails")

    def go_back(self):
        call_command("contract")
