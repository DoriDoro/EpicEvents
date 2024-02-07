from django.core.management import call_command
from django.core.management.base import BaseCommand

from cli.utils_menu import get_app_menu


class Command(BaseCommand):
    help = "Menu for all operations around the employees."

    def handle(self, *args, **options):
        choice = get_app_menu("employee")

        if choice == 1:
            call_command("employee_create")
        if choice == 2:
            call_command("employee_update")
        if choice == 3:
            call_command("employee_delete")
        if choice == 4:
            call_command("start")
