from django.core.management import call_command

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_tables import create_queryset_table


class Command(EpicEventsCommand):
    """
    Command to list all Clients.

    This command displays all Clients with get_create_model_table, finish the command and
    goes back to the client menu.

    Permissions for Employees with role:
        - SA: Sales
        - SU: Support
        - MA: Management
    """

    help = "Lists all clients."
    action = "LIST"
    permissions = ["SA", "SU", "MA"]

    def get_create_model_table(self):
        table_data = dict()

        queryset = Client.objects.select_related("employee").all()
        headers = ["", "employee", "email", "name"]

        for client in queryset:
            client_data = {
                "employee": client.employee.user.email,
                "email": client.email,
                "name": client.get_full_name,
            }
            table_data[f"Client {client.id}"] = client_data

        create_queryset_table(table_data, "Clients", headers=headers)

    def go_back(self):
        call_command("client")
