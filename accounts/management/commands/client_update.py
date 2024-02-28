from django.core.management import call_command

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import (
    create_pretty_table,
    create_queryset_table,
)


class Command(EpicEventsCommand):
    """
    This class `Command` is a subclass of `EpicEventsCommand` designed for updating client details
    within a system. It is specifically tailored for users with "SA" permissions, indicating that
    it is intended for sales.

    - `help`: A string describing the command's purpose, which is to prompt for details necessary
        to update a client.
    - `action`: A string indicating the action associated with this command, set to "UPDATE".
    - `permissions`: A list of roles that are allowed to execute this command, in this case, only
        "SA" (Sales) has the permission.

    Key methods within this class include:

    - `get_queryset`: Initializes the queryset for `Client` objects, selecting related `Employee`
        objects for each event.
    - `get_create_model_table`: Generates a table of all client emails to help the user select a
        client to update.
    - `get_requested_model`: Prompts the user to input the email address of the client they wish
        to update and displays the client's details for confirmation.
    - `get_fields_to_update`: Prompts the user to select which fields they want to update.
    - `get_available_fields`: Maps the selected fields to their corresponding input methods
        for data collection.
    - `get_data`: Collects the new data for the selected fields from the user.
    - `make_changes`: Updates the client with the new data.
    - `collect_changes`: Confirms the update of the client and displays a success message.
    - `go_back`: Provides an option to go back to the previous command, presumably to the main
        client management interface.

    This class encapsulates the functionality for updating client details, ensuring that only
    users with the appropriate permissions can perform this action. It leverages
    the `EpicEventsCommand` class for common command functionalities, such as displaying input
    prompts and handling user input.
    """

    help = "Prompts for details to to update a client."
    action = "UPDATE"
    permissions = ["SA"]

    def get_queryset(self):
        self.queryset = Client.objects.filter(employee__user=self.user).all()

    def get_create_model_table(self):
        table_data = dict()

        headers = [
            "",
            "** Client email **",
            "First name",
            "Last name",
            "Phone",
            "Company name",
        ]

        for client in self.queryset:
            client_data = {
                "email": client.email,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "phone": client.phone,
                "company_name": client.company_name,
            }
            table_data[f"Client {client.id}"] = client_data

        create_queryset_table(table_data, "my Clients", headers=headers)

    def get_requested_model(self):
        while True:
            self.display_input_title("Enter details:")

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
        self.display_input_title("Enter choice:")

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
        data = dict()
        for letter in self.fields_to_update:
            if self.available_fields[letter]:
                field_data = self.available_fields.get(letter)
                method = field_data["method"]
                params = field_data["params"]
                label = field_data["label"]

                data[label] = method(**params)
                self.fields.append(label)

        return data

    def make_changes(self, data):
        Client.objects.filter(email=self.object.email).update(**data)

        self.object.refresh_from_db()

        return self.object

    def collect_changes(self):
        self.fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "company_name",
        ]

        create_success_message("Client", "updated")
        super().collect_changes()

    def go_back(self):
        call_command("client")
