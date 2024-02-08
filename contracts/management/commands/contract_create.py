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

    update_table = list()

    def get_create_model_table(self):
        table_data = dict()
        create_model_table(Client, "email", "Client Emails")
        create_model_table(Employee, "user.email", "Employee Emails")

        queryset = Contract.objects.select_related("client").all()

        for contract in queryset:
            table_data[contract.client.id] = contract.client.email

        create_queryset_table(table_data, "Email", "Client Emails from contracts")

    def get_data(self):
        self.display_input_title("Enter details to create a new contract:")

        return {
            "client": self.email_input("Client email"),
            "employee": self.email_input("Employee email"),
            "total_costs": self.int_input("Amount of contract"),
            "amount_paid": self.int_input("Paid amount"),
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

        employee = Employee.objects.filter(user__email=data["employee"]).first()
        if not employee:
            create_does_not_exists_message("Employee")
            call_command("contract_create")

        validated_data["employee"] = employee

        # remove client and employee for data:
        data.pop("client", None)
        data.pop("employee", None)

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

    def display_changes(self):
        self.update_fields = [
            "total_costs",
            "amount_paid",
            "state",
        ]

        create_success_message("Contract", "created")
        self.update_table.append([f"Client: ", self.object.client.email])
        self.update_table.append([f"Employee: ", self.object.employee.user.email])
        super().display_changes()

    def go_back(self):
        call_command("contract")
