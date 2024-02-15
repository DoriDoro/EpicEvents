from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import (
    create_pretty_table,
    create_queryset_table,
)
from contracts.models import Contract


class Command(EpicEventsCommand):
    help = "Prompts for details to delete a contract."
    action = "DELETE"
    permissions = ["MA"]

    def get_create_model_table(self):
        table_data = dict()

        queryset = Contract.objects.select_related("client").all()

        for contract in queryset:
            table_data[contract.client.id] = contract.client.email

        create_queryset_table(table_data, "Client Emails from contracts", "Email")

    def get_requested_model(self):
        while True:
            self.display_input_title("Enter details:")

            email = self.email_input("Email address")
            self.object = Contract.objects.filter(client__email=email).first()

            if self.object:
                break
            else:
                create_invalid_error_message("email")

        self.stdout.write()
        contract_table = [
            ["Client: ", self.object.client.email],
            ["Employee: ", self.object.employee.user.email],
            ["Total costs: ", self.object.total],
            ["Amount paid: ", self.object.paid_amount],
            ["Rest amount: ", self.object.rest_amount],
            ["State: ", self.object.get_state_display()],
        ]
        create_pretty_table(contract_table, "Details of the Contract: ")

    def get_data(self):
        self.display_input_title("Enter choice:")

        return {
            "delete": self.choice_str_input(
                ("Y", "N"), "Choice to delete [Y]es or [N]o"
            ),
        }

    def make_changes(self, data):
        if data["delete"] == "Y":
            self.object.delete()
        if data["delete"] == "N":
            self.stdout.write()
            call_command("contract")

    def collect_changes(self):
        create_success_message("Contract", "deleted")

    def go_back(self):
        call_command("contract")
