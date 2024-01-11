from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Menu for all operations around the events."

    def handle(self, *args, **options):
        print("** Menu of the events **", end="\n\n")

        choice = 0
        while choice != 4:
            print(" *** Events Menu *** ")
            print("1) Create an event")
            print("2) Update an event")
            print("3) Delete an event")
            print("4) go back to Main Menu")
            choice = int(input("Please enter your choice: "))
            print()
