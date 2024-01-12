from django.core.management import call_command
from django.core.management.base import BaseCommand

from cli.menu import get_app_menu


class Command(BaseCommand):
    help = "Menu for all operations around the contracts."

    def handle(self, *args, **options):
        choice = get_app_menu("contract")

        if choice == 4:
            call_command("start")
