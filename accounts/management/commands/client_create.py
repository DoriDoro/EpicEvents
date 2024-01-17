from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Client

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to create a new client."

    def handle(self, *args, **options):
        while True:
            email = input(" Enter the email address: ")
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                self.stdout.write("   This email address is unknown. \n\n")

            else:
                create_client = {}
                for field in ["first_name", "last_name", "phone", "company_name"]:
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

                client_exists = Client.objects.filter(user=user).first()

                if client_exists:
                    self.stdout.write(f"   This client: {email} exists already! \n\n")
                else:
                    create_client["user"] = user
                    Client.objects.create(**create_client)

                    # TODO: display this info as table
                    self.stdout.write("\n   A new client was created. \n\n")
                    self.stdout.write(f"  Email: {email}")
                    self.stdout.write(f"  First name: {create_client['first_name']}")
                    self.stdout.write(f"  Last name: {create_client['last_name']}")
                    self.stdout.write(f"  Phone: {create_client['phone']}")
                    self.stdout.write(
                        f"  Company name: {create_client['company_name']} \n\n"
                    )
                    break
