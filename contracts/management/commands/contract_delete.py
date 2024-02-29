import sys

from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import (
    create_pretty_table,
    create_queryset_table,
)
from contracts.models import Contract


class Command(EpicEventsCommand):
    """
    This class `Command` is a subclass of `EpicEventsCommand` designed for managing contract
    deletions within a system. It is specifically tailored for users with "MA" permissions,
    indicating that it is intended for managers.

    - `help`: A string describing the command's purpose, which is to prompt for details necessary
        to delete a contract.
    - `action`: A string indicating the action associated with this command, set to "DELETE".
    - `permissions`: A list of roles that are allowed to execute this command, in this case, only
        "MA" (Management) has the permission.

    Key methods within this class include:

    - `get_create_model_table`: Generates a table of all contracts to help the user select a
        contract to delete.
    - `get_requested_model`: Prompts the user to input the email address of the client from
        the contract they wish to delete and displays the contract's details for confirmation.
    - `get_data`: Prompts the user to confirm the deletion of the selected contract.
    - `make_changes`: If the user confirms the deletion, it proceeds to delete the contract;
        otherwise, it cancels the operation and returns to the contract management interface.
    - `collect_changes`: Confirms the deletion of the contract and displays a success message.
    - `go_back`: Provides an option to go back to the previous command, presumably to the main
        contract management interface.

    This class encapsulates the functionality for deleting contracts, ensuring that only users with
    the appropriate permissions can perform this action. It leverages
    the `EpicEventsCommand` class for common command functionalities, such as displaying input
    prompts and handling user input.
    """

    help = "Prompts for details to delete a contract."
    action = "DELETE"
    permissions = ["MA"]

    def get_queryset(self):
        self.queryset = (
            Contract.objects.select_related("client").only("client__email").all()
        )

    def get_instance_data(self):
        super().get_instance_data()
        table_data = dict()

        for contract in self.queryset:
            contract_data = {
                "client": contract.client.email,
                "total": contract.total,
                "paid": contract.paid_amount,
                "rest": contract.rest_amount,
                "state": contract.get_state_display(),
            }
            table_data[f"Contract {contract.id}"] = contract_data

        create_queryset_table(
            table_data, "Contracts", headers=self.headers["contract"][0:6]
        )

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
            sys.exit()

    def collect_changes(self):
        create_success_message("Contract", "deleted")

    def go_back(self):
        call_command("contract")
