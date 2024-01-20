from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import Client
from cli.input_utils import customer_input
from cli.menu_utils import create_menu
from cli.table_utils import create_pretty_table


class Command(BaseCommand):
    help = "Prompts for details to update a client."

    def handle(self, *args, **options):
        updates_of_client = {}

        client_fields = {
            1: "email",
            2: "first_name",
            3: "last_name",
            4: "phone",
            5: "company_name",
            6: "quit",
        }

        update_client_list = []
        email_all_clients = []

        get_all_clients = Client.objects.all()

        for client in get_all_clients:
            all_clients_table = ["Email: ", client.email]
            email_all_clients.append(all_clients_table)

        # display all users
        create_pretty_table("All clients: ", email_all_clients)

        while True:
            email = customer_input("email address")
            client = Client.objects.filter(email=email).first()

            if client is None:
                self.stdout.write("   This email address is unknown. \n\n")
            else:
                self.stdout.write()
                client_table = [
                    ["Email: ", email],
                    ["First name: ", client.first_name],
                    ["Last name: ", client.last_name],
                    ["Phone: ", client.phone],
                    ["Company name: ", client.company_name],
                ]

                create_pretty_table("Details about this client: ", client_table)

                menu_choices = {
                    1: "Email",
                    2: "First name",
                    3: "Last name",
                    4: "Phone number",
                    5: "Company name",
                    6: "quit",
                }
                create_menu("Which details you want to update? ", menu_choices)

                update_str = input(
                    " Which details you want to update? (several numbers possible): "
                )
                update_list = [int(num) for num in update_str.split()]

                for key, field in client_fields.items():
                    for number in update_list:
                        if key == number:
                            update_client_list.append(field)

                for field in update_client_list:
                    if field == "quit":
                        call_command("client")
                        break
                    if field == "phone":
                        while True:
                            try:
                                updates_of_client[field] = int(
                                    input(f"\n  Please enter the new {field}: ")
                                )
                                break
                            except ValueError:
                                self.stdout.write("    Invalid input. \n\n")
                    else:
                        updates_of_client[field] = input(
                            f"  Please enter the new {field}: "
                        )

                if updates_of_client:
                    Client.objects.filter(email=email).update(**updates_of_client)
                    self.stdout.write("   The client was updated. \n\n")
                    call_command("client")
                    break
                else:
                    self.stdout.write("  No changes made. \n\n")
                    call_command("client")
                    break
