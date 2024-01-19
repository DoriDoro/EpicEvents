from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from tabulate import tabulate

from cli.input_utils import customer_input

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to create a new user."

    def handle(self, *args, **options):
        while True:
            email = customer_input("email address")
            user = UserModel.objects.filter(email=email).first()
            if user is not None:
                self.stdout.write("  Sorry, this user exists already! \n\n")
                self.stdout.flush()
            else:
                password = customer_input("password")
                call_command("user_create", email, password)
                self.stdout.write()
                self.stdout.write("   A new user was created. \n")

                display_password = "*" * 10
                table = [["Email:", email], ["Password:", display_password]]
                table = tabulate(table, tablefmt="pretty")
                indented_table = "\n".join("  " + line for line in table.split("\n"))
                self.stdout.write(indented_table)

                call_command("user")
                break
