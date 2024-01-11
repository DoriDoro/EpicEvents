from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Menu for all operations around the contracts."

    def handle(self, *args, **options):
        print("** Menu of the contracts **", end="\n\n")

        choice = 0
        while choice != 4:
            print(" *** Contracts Menu *** ")
            print("  [1] Create a contract")
            print("  [2] Update a contract")
            print("  [3] Delete a contract")
            print("  [4] go back to Main Menu")
            choice = int(input("Please enter your choice: "))
            print()
