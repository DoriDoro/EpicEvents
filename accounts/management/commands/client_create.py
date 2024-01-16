from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Client

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to create a new client."

    def handle(self, *args, **options):
        while True:
            email = input(" Please enter the email address of the future client: ")
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                self.stdout.write(
                    "   This email address is not known. Please enter a valid email address. \n\n"
                )
            else:
                # get all attributes of the model Client
                fields = [f.name for f in Client._meta.fields]
                updates = {}
                for field in fields:
                    if field in ["first_name", "last_name", "phone", "company_name"]:
                        updates[field] = input(f"Please enter the {field}: ")

                client_exists = Client.objects.filter(user=user).first()

                if client_exists:
                    self.stdout.write(
                        f"   This client: {email} exists already! "
                        f"Please choose an other email address to create a new client. \n\n"
                    )
                else:
                    updates["user"] = user
                    Client.objects.create(**updates)

                    self.stdout.write("\n\n   A new client was created. \n\n")
                    self.stdout.write(f"    Email: {email}")
                    self.stdout.write(f"    First name: {updates['first_name']}")
                    self.stdout.write(f"    Last name: {updates['last_name']}")
                    self.stdout.write(f"    Phone: {updates['phone']}")
                    self.stdout.write(
                        f"    Company name: {updates['company_name']} \n\n"
                    )
                    break
