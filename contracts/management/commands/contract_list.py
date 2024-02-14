from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_queryset_table
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
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        table_data = dict()

        queryset = Contract.objects.select_related("client", "employee").all()
        headers = [
            "",
            "employee",
            "client",
            "total amount",
            "amount paid",
            "rest amount",
            "state",
        ]

        for contract in queryset:
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

    def go_back(self):
        call_command("contract")
