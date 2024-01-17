from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import Client


class Command(BaseCommand):
    help = "Prompts for details to update a client."

    def handle(self, *args, **options):
        updates_of_client = {}

        client_fields = {
            1: "first_name",
            2: "last_name",
            3: "phone",
            4: "company_name",
            5: "quit",
        }

        update_client_list = []

        while True:
            email = input(" Enter the email address: ")
            client = Client.objects.filter(user__email=email).first()
            if client is None:
                self.stdout.write("   This email address is unknown. \n\n")
            else:
                # TODO: use a table to display this info
                self.stdout.write("\n   Details about this client:")
                self.stdout.write(f"    Email: {email}")
                self.stdout.write(f"    First name: {client.first_name}")
                self.stdout.write(f"    Last name: {client.last_name}")
                self.stdout.write(f"    Phone: {client.phone}")
                self.stdout.write(f"    Company name: {client.company_name} \n\n")

                # TODO: use a table to display this info
                self.stdout.write("   Which details you want to update?")
                self.stdout.write("    [1] first name")
                self.stdout.write("    [2] last name")
                self.stdout.write("    [3] phone number")
                self.stdout.write("    [4] company name")
                self.stdout.write("    [5] go back to Main Menu \n\n")

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
                        call_command("start")
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
                    Client.objects.filter(user__email=email).update(**updates_of_client)
                    self.stdout.write("   The client was updated. \n\n")
                    break
                else:
                    self.stdout.write("  No changes made. \n\n")
                    break
