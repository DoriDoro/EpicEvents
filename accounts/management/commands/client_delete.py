from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import Client


class Command(BaseCommand):
    help = "Prompts for details to delete a client."

    def handle(self, *args, **options):
        while True:
            email = input(" Enter the email address: ")
            client = Client.objects.filter(user__email=email).first()
            if client is None:
                self.stdout.write("   This email address is unknown. \n\n")
            else:
                delete_client = input(
                    f"  Do you want to delete this client {email}? (yes/no): "
                ).lower()

                if delete_client in ["yes", "y"]:
                    client.delete()
                    self.stdout.write(f"\n  The client {email} was deleted! \n\n")
                    break
                if delete_client in ["no", "n"]:
                    possible_exit = input(
                        "   Do you want to delete an other employee (yes) "
                        "or do you want to go back to the main menu? (*): "
                    )
                    if possible_exit == "*":
                        call_command("start")
                        break
                else:
                    self.stdout.write("   Invalid input.")
