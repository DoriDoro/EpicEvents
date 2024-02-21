from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_permission_denied_message
from cli.utils_tables import create_queryset_table, create_pretty_table
from contracts.models import Contract


class Command(EpicEventsCommand):
    """
    Command to list all Contracts.

    This command displays all Contracts with get_create_model_table, finish the command and
    goes back to the contract menu.

    Permissions for Employees with role:
        - SA: Sales
        - SU: Support
        - MA: Management
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
            "Employee email",
            "Client email",
            "Total amount",
            "Amount paid",
            "Rest amount",
            "State",
        ]

        for contract in self.queryset:
            contract_data = {
                "employee": contract.employee.user.email,
                "client": contract.client.email,
                "total": contract.total,
                "paid": contract.paid_amount,
                "rest": contract.rest_amount,
                "state": contract.get_state_display(),
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
            call_command("client")
            return
        elif choice["filter"] == "N":
            self.stdout.write()
            call_command("client")
            return

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
        return self.queryset.filter(employee__user=self.user)
        # TODO: SA and MA can filter, user_queryset has to be SA, even MA is filtering

    def filter_selected_fields(self, selected_fields, order, user_queryset):
        field_mapping = {
            "C": "client",
            "T": "total_amount",
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

        headers = ["", "client", "total amount", "amount paid", "state"]

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
