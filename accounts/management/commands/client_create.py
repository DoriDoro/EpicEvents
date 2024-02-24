from django.core.management import call_command
from django.db import IntegrityError

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_error_message, create_success_message
from cli.utils_tables import create_queryset_table


class Command(EpicEventsCommand):
    """
    This class `Command` is a subclass of `EpicEventsCommand` designed to facilitate the creation
    of new clients within a system. It is specifically tailored for users with "SA" permissions,
    indicating that it is intended for sales.

    - `help`: A string describing the command's purpose, which is to prompt for details necessary
        to create a new client.
    - `action`: A string indicating the action associated with this command, set to "CREATE".
    - `permissions`: A list of roles that are allowed to execute this command, in this case, only
        "SA" (Sales) has the permission.

    Key methods within this class include:

    - `get_queryset`: Initializes the queryset for `Client` objects, selecting related `Employee`
        objects for each client.
    - `get_create_model_table`: Generates tables of all clients and a subset of clients related to
        the current user, displaying relevant information such as email, first name, last name,
        company name, and employee.
    - `get_data`: Prompts the user to input details for creating a new client, capturing email,
        first name, last name, phone number, and company name.
    - `make_changes`: Attempts to create a new `Client` object with the provided data, associating
        it with the current user's `Employee` object. Handles potential `IntegrityError` by
        displaying an error message and re-prompting the user to create a client.
    - `collect_changes`: Confirms the creation of a new client and displays a success message.
    - `go_back`: Provides an option to go back to the previous command, presumably to the main
        client management interface.

    This class encapsulates the functionality for creating new clients, ensuring that only users
    with the appropriate permissions can perform this action. It leverages the `EpicEventsCommand`
    class for common command functionalities, such as displaying input prompts
    and handling user input.
    """

    help = "Prompts for details to create a new client."
    action = "CREATE"
    permissions = ["SA"]

    def get_queryset(self):
        self.queryset = Client.objects.select_related("employee").all()

    def get_create_model_table(self):
        all_clients_data = dict()
        my_clients_data = dict()
        headers_all = [
            "",
            "** Client email **",
            "First name",
            "Last name",
            "Company name",
            "Employee",
        ]
        headers_my = [
            "",
            "** Client email **",
            "First name",
            "Last name",
            "Company name",
        ]

        for client in self.queryset:
            client_data = {
                "email": client.email,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "company_name": client.company_name,
                "employee": client.employee,
            }

            all_clients_data[f"Client {client.id}"] = client_data

            if client.employee.user == self.user:
                # create a copy of 'client_date' otherwise the column 'Employee' is empty
                client_data = client_data.copy()
                client_data.pop("employee", None)
                my_clients_data[f"Client {client.id}"] = client_data

        create_queryset_table(all_clients_data, "Clients", headers=headers_all)
        create_queryset_table(my_clients_data, "my Clients", headers=headers_my)

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
        self.fields = [
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
