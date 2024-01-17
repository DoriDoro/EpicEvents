from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import Client

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to create a new client."

    def handle(self, *args, **options):
        while True:
            create_client = {}
            for field in ["email", "first_name", "last_name", "phone", "company_name"]:
                if field == "phone":
                    while True:
                        try:
                            create_client[field] = int(
                                input(f"  Please enter the {field}: ")
                            )
                            break
                        except ValueError:
                            self.stdout.write("    Invalid input. \n\n")
                else:
                    create_client[field] = input(f"  Please enter the {field}: ")

            client_email = create_client["email"]
            client_exists = Client.objects.filter(email=client_email).first()

            if client_exists:
                self.stdout.write(
                    f"   This client: {client_email} exists already! \n\n"
                )
            else:
                Client.objects.create(**create_client)

                # TODO: display this info as table
                self.stdout.write("\n   A new client was created. \n\n")
                self.stdout.write(f"  Email: {client_email}")
                self.stdout.write(f"  First name: {create_client['first_name']}")
                self.stdout.write(f"  Last name: {create_client['last_name']}")
                self.stdout.write(f"  Phone: {create_client['phone']}")
                self.stdout.write(
                    f"  Company name: {create_client['company_name']} \n\n"
                )
                call_command("client")
                break
