from django.core.management import call_command
from django.db import transaction

from accounts.models import Employee
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import (
    create_success_message,
    create_invalid_error_message,
)
from cli.utils_tables import (
    create_queryset_table,
    create_pretty_table,
)
from contracts.models import Contract


class Command(EpicEventsCommand):
    help = "Prompts for details to update a contract."
    action = "UPDATE"

    update_fields = list()
    update_table = list()

    def get_create_model_table(self):
        table_data = dict()

        queryset = Contract.objects.select_related("client").all()

        for contract in queryset:
            table_data[contract.client.id] = contract.client.email

        create_queryset_table(table_data, "Email", "Client Emails from contracts")

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
            ["[E]mployee: ", self.object.employee.user.email],
            ["[T]otal costs in €: ", self.object.total_costs],
            ["[A]mount paid in €: ", self.object.amount_paid],
            ["[S]tate: ", self.object.get_state_display()],
        ]
        create_pretty_table(contract_table, "Details of the Contract: ")

    def get_fields_to_update(self):
        self.display_input_title("Enter choice:")

        self.fields_to_update = self.multiple_choice_str_input(
            ("E", "T", "A", "S"), "Your choice? [E, T, A, S]"
        )

    def get_available_fields(self):
        self.available_fields = {
            "E": {
                "method": self.email_input,
                "params": {"label": "Employee Email"},
                "label": "employee_email",
            },
            "T": {
                "method": self.int_input,
                "params": {"label": "Total amount"},
                "label": "total_costs",
            },
            "A": {
                "method": self.int_input,
                "params": {"label": "Amount paid"},
                "label": "amount_paid",
            },
            "S": {
                "method": self.choice_str_input,
                "params": {"options": ("S", "D"), "label": "State [S]igned or [D]raft"},
                "label": "state",
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
                self.update_fields.append(label)

        return data

    @transaction.atomic
    def make_changes(self, data):
        employee_email = data.pop("employee_email", None)
        employee = Employee.objects.filter(user__email=employee_email).first()

        if employee_email:
            contract = self.object
            contract.employee = employee
            contract.save()

        Contract.objects.filter(client=self.object.client).update(**data)

        # Refresh the object from the database
        self.object.refresh_from_db()

        return self.object

    def display_changes(self):
        self.update_fields = [
            "total_costs",
            "amount_paid",
            "state",
        ]

        create_success_message("Contract", "updated")
        self.update_table.append([f"Client: ", self.object.client.email])
        self.update_table.append([f"Employee: ", self.object.employee.user.email])
        super().display_changes()

    def go_back(self):
        call_command("contract")
