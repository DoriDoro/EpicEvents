from django.core.management import call_command

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import (
    create_does_not_exists_message,
    create_error_message,
    create_success_message,
)
from cli.utils_tables import create_queryset_table
from events.models import Event


class Command(EpicEventsCommand):
    help = "Prompts for details to create a new event"
    action = "CREATE"
    permissions = ["SA"]

    def get_queryset(self):
        self.queryset = Event.objects.select_related("contract__client").all()

    def get_create_model_table(self):
        all_events_data = dict()
        my_events_data = dict()
        headers_all = [
            "",
            "** Client email **",
            "Date",
            "Name",
            "Location",
            "Max guests",
            "Employee",
        ]
        headers_my = headers_all[0:6]

        for event in self.queryset:
            event_data = {
                "email": event.contract.client.email,
                "date": event.date.strftime("%d/%m/%Y"),
                "name": event.name,
                "location": event.location,
                "max_guests": event.max_guests,
                "employee": event.employee,
            }

            all_events_data[f"Event {event.id}"] = event_data

            if event.contract.client.employee.user == self.user:
                event_data = event_data.copy()
                event_data.pop("employee", None)
                my_events_data[f"Events {event.id}"] = event_data

        create_queryset_table(all_events_data, "Events", headers=headers_all)
        create_queryset_table(my_events_data, "my Events", headers=headers_my)

    def get_data(self):
        self.display_input_title("Enter the details to create a new event:")

        return {
            "client": self.email_input("Client email"),
            "date": self.date_input("Date of the event [DD/MM/YYYY]"),
            "name": self.text_input("Name of the event"),
            "location": self.text_input("Location of the event"),
            "max_guests": self.int_input("Number of guests"),
            "notes": self.text_input("Any notes?"),
        }

    def make_changes(self, data):
        validated_data = dict()

        client = (
            Client.objects.filter(email=data["client"])
            .select_related("employee")
            .first()
        )  # get info of client and employee

        if not client:
            create_does_not_exists_message("Client")
            call_command("event_create")

        validated_data["client"] = client
        validated_data["employee"] = client.employee

        # remove client from data:
        data.pop("client", None)

        # verify if event already exists:
        event_exists = Event.objects.filter(
            contract=validated_data["client"], name=data["name"]
        ).exists()

        if event_exists:
            create_error_message("Event")
            call_command("event_create")

        # create new event:
        self.object = Event.objects.create(
            contract=validated_data["client"],
            employee=validated_data["employee"],
            **data,
        )

    def collect_changes(self):
        self.fields = ["name", "location", "max_guests", "notes"]

        create_success_message("Event", "created")

        self.update_table.append([f"Client: ", self.object.contract.client.email])
        self.update_table.append([f"Employee: ", self.object.employee.user.email])
        self.update_table.append([f"Date: ", self.object.date.strftime("%d/%m/%Y")])
        super().collect_changes()

    def go_back(self):
        call_command("event")
