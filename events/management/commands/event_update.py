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
from events.models import Event


class Command(EpicEventsCommand):
    help = "Prompts for details to update an event"
    action = "UPDATE"

    def get_create_model_table(self):
        table_data = dict()

        queryset = Event.objects.select_related("contract__client").all()
        for event in queryset:
            table_data[event.contract.client.id] = event.contract.client.email

        create_queryset_table(table_data, "Email", "Client Emails from Events")

    def get_requested_model(self):
        while True:
            self.display_input_title("Enter details:")

            email = self.email_input("Email address of client")
            self.object = Event.objects.filter(contract__client__email=email).first()

            if self.object:
                break
            else:
                create_invalid_error_message("email")

        self.stdout.write()
        event_table = [
            ["Client: ", self.object.contract.client.email],
            ["[E]mployee: ", self.object.employee.user.email],
            ["[D]ate: ", self.object.date.strftime("%d/%m/%Y")],
            ["[N]ame: ", self.object.name],
            ["[L]ocation: ", self.object.location],
            ["number of [G]uests: ", self.object.max_guests],
            ["[No]tes: ", self.object.notes],
        ]
        create_pretty_table(event_table, "Details of the Event: ")

    def get_fields_to_update(self):
        self.display_input_title("Enter choice:")

        self.fields_to_update = self.multiple_choice_str_input(
            ("E", "D", "N", "L", "G", "No"), "Your choice? [E, D, N, L, G, No]"
        )

    def get_available_fields(self):
        self.available_fields = {
            "E": {
                "method": self.email_input,
                "params": {"label": "Employee Email"},
                "label": "employee_email",
            },
            "D": {
                "method": self.date_input,
                "params": {"label": "Date of the event"},
                "label": "date",
            },
            "N": {
                "method": self.text_input,
                "params": {"label": "Name of event"},
                "label": "name",
            },
            "L": {
                "method": self.text_input,
                "params": {"label": "Location of the event"},
                "label": "location",
            },
            "G": {
                "method": self.text_input,
                "params": {"label": "Number of guest"},
                "label": "max_guests",
            },
            "No": {
                "method": self.text_input,
                "params": {"label": "Notes of the event"},
                "label": "notes",
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
            event = self.object
            event.employee = employee
            event.save()

        Event.objects.filter(contract__client=self.object.contract.client).update(
            **data
        )

        # Refresh the object from the database
        self.object.refresh_from_db()

        return self.object

    def display_changes(self):
        self.update_fields = ["name", "location", "max_guests", "notes"]

        create_success_message("Event", "created")

        self.update_table.append([f"Client: ", self.object.contract.client.email])
        self.update_table.append([f"Employee: ", self.object.employee.user.email])
        self.update_table.append([f"Date: ", self.object.date.strftime("%d/%m/%Y")])
        super().display_changes()

    def go_back(self):
        call_command("event")
