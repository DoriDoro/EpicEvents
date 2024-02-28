import sys

from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_permission_denied_message
from cli.utils_tables import create_queryset_table, create_pretty_table
from contracts.models import Contract


class Command(EpicEventsCommand):
    """
    This class `Command` is a subclass of `EpicEventsCommand` designed to list all contracts with
    an option to filter the list based on user input. It is accessible to users with "SA", "SU", or
    "MA" permissions.

    - `help`: A string describing the command's purpose, which is to list all contracts
        and optionally filter them.
    - `action`: A string indicating the action associated with this command, set to "LIST_FILTER".
    - `permissions`: A list of roles that are allowed to execute this command, in this case, "SA"
        (Sales), "SU" (Support), and "MA" (Management) have the permission.

    Key methods within this class include:

    - `get_queryset`: Initializes the queryset for `Contract` objects, selecting related `Client`
        and `Employee` objects for each contract.
    - `get_create_model_table`: Generates a table of all contracts, displaying relevant information
        such as email, total amount, paid amount, the rest amount, state and employee.
    - `get_data`: Prompts the user to decide whether they want to filter contracts,
        capturing their choice.
    - `user_choice`: Handles the user's choice to filter contracts, with special handling for "SA"
        and "MA" role to allow filtering without permission denied messages.
    - `choose_attributes`: Displays fields available for filtering and allows the user to select
        which fields they want to filter by.
    - `request_field_selection`: Prompts the user to select specific fields for filtering and to
        choose the order (ascending or descending).
    - `get_user_queryset`: Filters the queryset based on the user's selection and order preference.
    - `filter_selected_fields`: Applies the selected filters and order to the queryset, preparing
        it for display.
    - `display_result`: Displays the filtered and ordered list of contracts to the user.
    - `go_back`: Provides an option to go back to the previous command, presumably to the main
        contract management interface.

    This class encapsulates the functionality for listing and optionally filtering contract,
    ensuring that only users with the appropriate permissions can perform these actions.
    It leverages the `EpicEventsCommand` class for common command functionalities, such as
    displaying input prompts and handling user input.
    """

    help = "Lists all contracts."
    action = "LIST_FILTER"
    permissions = ["SA", "SU", "MA"]

    def get_queryset(self):
        self.queryset = Contract.objects.select_related("client", "employee").all()

    def get_create_model_table(self):
        table_data = dict()

        headers = [
            "",
            "** Client email **",
            "Total amount",
            "Amount paid",
            "Rest amount",
            "State",
            "Employee",
        ]

        for contract in self.queryset:
            contract_data = {
                "client": contract.client.email,
                "total": contract.total,
                "paid": contract.paid_amount,
                "rest": contract.rest_amount,
                "state": contract.get_state_display(),
                "employee": contract.employee,
            }
            table_data[f"Contract {contract.id}"] = contract_data

        create_queryset_table(table_data, "Contracts", headers=headers)

    def get_data(self):
        self.display_input_title("Enter choice:")

        return {
            "filter": self.choice_str_input(
                ("Y", "N"), "Do you want to filter your clients? [Y]es or [N]o"
            ),
        }

    def user_choice(self, choice):
        if choice["filter"] == "Y" and self.user.employee_users.role in ["SA", "MA"]:
            self.stdout.write()
            return
        elif choice["filter"] == "Y":
            create_permission_denied_message()
            call_command("contract")
            sys.exit()
        elif choice["filter"] == "N":
            self.stdout.write()
            call_command("contract")
            sys.exit()

    def choose_attributes(self):
        self.fields = ["client", "total_amount", "amount_paid", "state"]

        client_table = []
        for field in self.fields:
            field = field.replace("_", " ")
            formatted_field = [f"[{field[0].upper()}]{field[1:]}"]
            client_table.append(formatted_field)
        create_pretty_table(client_table, "Which fields you want to filter?")

    def request_field_selection(self):
        self.display_input_title("Enter choice:")

        selected_fields = self.multiple_choice_str_input(
            ("C", "T", "A", "S"), "Your choice? [C, T, A, S]"
        )
        # ascending or descending
        order = self.choice_str_input(
            ("A", "D"), "Your choice? [A]scending or [D]ecending"
        )
        self.stdout.write()
        return selected_fields, order

    def get_user_queryset(self):
        # if an MA employee is authenticated, create a queryset with all SA employees
        if self.user.employee_users.role == "MA":
            return self.queryset.filter(employee__role="SA")

        # if an SA employee is authenticated, create queryset of this SA employee
        return self.queryset.filter(employee__user=self.user)

    def filter_selected_fields(self, selected_fields, order, user_queryset):
        field_mapping = {
            "C": "client",
            "T": "total_costs",
            "A": "amount_paid",
            "S": "state",
        }

        order_by_fields = [
            f"{'-' if order == 'D' else ''}{field_mapping[field]}"
            for field in selected_fields
        ]

        filter_queryset = user_queryset.order_by(*order_by_fields)

        return filter_queryset, order_by_fields

    def display_result(self, filter_queryset, order_by_fields):
        table_data = dict()

        headers = ["", "** Client email **", "Total amount", "Amount paid", "State"]

        for contract in filter_queryset:
            client_data = {
                "client": contract.client.email,
                "total_amount": contract.total_costs,
                "amount_paid": contract.amount_paid,
                "state": contract.state,
            }
            table_data[f"Contract {contract.id}"] = client_data

        create_queryset_table(
            table_data, "my Contracts", headers=headers, order_by_fields=order_by_fields
        )

    def go_back(self):
        call_command("contract")
