from django.core.management.base import BaseCommand
from django.core.management import call_command

from cli.menu import get_start_menu


class Command(BaseCommand):
    help = "Start of the program."

    def handle(self, *args, **options):
        choice = get_start_menu("Epic Events")

        if choice == 1:
            call_command("employee")
        if choice == 2:
            call_command("client")
        if choice == 3:
            call_command("contract")
        if choice == 4:
            call_command("event")
