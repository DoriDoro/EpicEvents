from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_model_table
from contracts.models import Contract


class Command(EpicEventsCommand):
    help = "Lists all contracts."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        # TODO: more details of the contracts [client, total, paid_amount, rest_amount, state]
        create_model_table(Contract, "client.email", "Client emails")

    def go_back(self):
        call_command("contract")
