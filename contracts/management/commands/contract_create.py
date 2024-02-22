from django.core.management import call_command

from accounts.models import Client, Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import (
    create_error_message,
    create_does_not_exists_message,
    create_success_message,
)
from cli.utils_tables import create_model_table, create_queryset_table
from contracts.models import Contract


class Command(EpicEventsCommand):
    help = "Prompts for details to create a new contract."
    action = "CREATE"
    permissions = ["MA"]

    def get_queryset(self):
        """
        Not using the EpicEventsCommand get_queryset method because only used for the creation
        of a contract.

        Returns:
            A queryset of the Contract model, with all ForeignKey relations.
        """
        self.queryset = Contract.objects.select_related("client").all()

    def get_create_model_table(self):
        all_clients_data = dict()
        all_contracts_data = dict()
        headers_clients = [
            "",
            "** Client email **",
            "First name",
            "Last name",
            "Company name",
            "Employee",
        ]
        headers_contracts = [
            "",
            "** Client email **",
            "Total costs",
            "Amount paid",
            "State",
            "Employee",
        ]

        for contract in self.queryset:
            contract_data = {
                "email": contract.client.email,
                "total_costs": contract.total_costs,
                "amount_paid": contract.paid_amount,
                "state": contract.state,
                "employee": contract.client.employee.user.email,
            }
            client_data = {
                "email": contract.client.email,
                "first_name": contract.client.first_name,
                "last_name": contract.client.last_name,
                "company_name": contract.client.company_name,
                "employee": contract.client.employee.user.email,
            }

            all_clients_data[f"Client {contract.client.id}"] = client_data
            all_contracts_data[f"Contract {contract.id}"] = contract_data

        create_queryset_table(all_clients_data, "Clients", headers=headers_clients)
        create_queryset_table(all_contracts_data, "Clients", headers=headers_contracts)

    def get_data(self):
        self.display_input_title("Enter details to create a new contract:")

        return {
            "client": self.email_input("Client email"),
            "total_costs": self.decimal_input("Amount of contract"),
            "amount_paid": self.decimal_input("Paid amount"),
            "state": self.choice_str_input(("S", "D"), "State [S]igned or [D]raft"),
        }

    def make_changes(self, data):
        validated_data = dict()
        # verify if the contract already exists, client + contract
        # OneToOne instead of ForeignKey? client

        client = Client.objects.filter(email=data["client"]).first()
        if not client:
            create_does_not_exists_message("Client")
            call_command("contract_create")

        validated_data["client"] = client
        validated_data["employee"] = client.employee

        # remove client and employee for data:
        data.pop("client", None)

        # verify if the contract already exists:
        contract_exists = Contract.objects.filter(
            client=validated_data["client"]
        ).exists()
        if contract_exists:
            create_error_message("Contract")
            call_command("contract_create")

        # create the contract:
        self.object = Contract.objects.create(
            client=validated_data["client"],
            employee=validated_data["employee"],
            **data,
        )

    def collect_changes(self):
        self.fields = [
            "total",
            "paid_amount",
            "rest_amount",
            "state",
        ]

        create_success_message("Contract", "created")
        self.update_table.append([f"Client: ", self.object.client.email])
        self.update_table.append([f"Employee: ", self.object.employee.user.email])
        super().collect_changes()

    def go_back(self):
        call_command("contract")
