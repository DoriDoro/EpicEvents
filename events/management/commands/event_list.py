from django.core.management import call_command

from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_queryset_table
from events.models import Event


class Command(EpicEventsCommand):
    """
    Command to list all Events.

    This command displays all Events with get_create_model_table, finish the command and
    goes back to the event menu.

    Permissions for Employees with role:
        - SA: Sales
        - SU: Support
        - MA: Management
    """

    help = "Lists all events."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        table_data = dict()

        queryset = Event.objects.select_related("contract", "employee").all()
        headers = [
            "",
            "employee",
            "client",
            "date",
            "name",
            "location",
            "max_guests",
        ]

        for event in queryset:
            event_data = {
                "employee": event.employee.user.email,
                "client": event.contract.client.email,
                "date": event.date,
                "name": event.name,
                "location": event.location,
                "max_guests": event.max_guests,
            }
            table_data[f"Event {event.id}"] = event_data

        create_queryset_table(table_data, "Events", headers=headers)

    def go_back(self):
        call_command("contract")
