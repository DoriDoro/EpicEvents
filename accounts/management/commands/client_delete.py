from django.core.management import call_command

from accounts.models import Client
from cli.utils_custom_command import EpicEventsCommand
from cli.utils_messages import create_success_message
from cli.utils_tables import create_model_table, create_pretty_table


class Command(EpicEventsCommand):
    help = "Prompts for details to delete a client."
    action = "DELETE"
    permissions = ["MA"]

    def get_create_model_table(self):
        create_model_table(Client, "email", "Client Emails")

    def get_requested_model(self):
        self.display_input_title("Enter details:")

        email = self.email_input("Email address")
        self.stdout.write()
        self.object = Client.objects.filter(email=email).first()

        client_table = [
            ["Email: ", self.object.email],
            ["First name: ", self.object.first_name],
            ["Last name: ", self.object.last_name],
            ["Phone: ", self.object.phone],
            ["Company name: ", self.object.company_name],
        ]

        create_pretty_table(client_table, "Details of the Client: ")

    def get_data(self):
        self.display_input_title("Enter choice:")

        return {
            "delete": self.choice_str_input(
                ("Y", "N"), "Choice to delete [Y]es or [N]o?"
            )
        }

    def make_changes(self, data):
        if data["delete"] == "Y":
            self.object.delete()
        if data["delete"] == "N":
            self.stdout.write()
            call_command("client")

    def collect_changes(self):
        create_success_message("Client", "deleted")

    def go_back(self):
        call_command("client")
