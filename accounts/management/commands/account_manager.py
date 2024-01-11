from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Menu for all operations around the account managers."

    def handle(self, *args, **options):
        print("** Menu of the account managers **", end="\n\n")

        choice = 0
        while choice != 4:
            print(" *** Account Manager Menu *** ")
            print("1) Create an Account Manager")
            print("2) Update an Account Manager")
            print("3) Delete an Account Manager")
            print("4) go back to Main Menu")
            choice = int(input("Please enter your choice: "))
            print()

            # if choice == 1:
            #     call_command(
            #         "create_account_manager",
            #         user=1,
            #         first_name="John",
            #         last_name="Doe",
            #         role="Management",
            #     )
