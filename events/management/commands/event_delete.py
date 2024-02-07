from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message, create_invalid_error_message
from cli.utils_tables import (
    create_pretty_table,
    create_queryset_table,
)
from events.models import Event


class Command(EpicEventsCommand):
    help = "Prompts for details to delete an event."
    action = "DELETE"

    def get_create_model_table(self):
        table_data = dict()

        queryset = Event.objects.select_related("contract__client").all()
        for event in queryset:
            table_data[event.contract.client.id] = event.contract.client.email

        create_queryset_table(table_data, "Email", "Client Emails from Events")

    def get_requested_model(self):
        while True:
            email = self.email_input("Email address of client")
            self.object = Event.objects.filter(contract__client__email=email).first()

            if self.object:
                break
            else:
                create_invalid_error_message("email")

        self.stdout.write()
        event_table = [
            ["Client: ", self.object.contract.client.email],
            ["Employee: ", self.object.employee.user.email],
            ["Date: ", self.object.date.strftime("%d/%m/%Y")],
            ["Name: ", self.object.name],
            ["Location: ", self.object.location],
            ["number of Guests: ", self.object.max_guests],
            ["Notes: ", self.object.notes],
        ]
        create_pretty_table(event_table, "Details of the Event: ")

    def get_data(self):
        return {
            "delete": self.choice_str_input(
                ("Y", "N"), "Choice to delete [Y]es or [N]o"
            ),
        }

    def make_changes(self, data):
        if data["delete"] == "Y":
            self.object.delete()
        if data["delete"] == "N":
            self.stdout.write()
            call_command("event")

    def display_changes(self):
        create_success_message("Event", "deleted")

    def go_back(self):
        call_command("event")
