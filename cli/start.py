from django.core.management import call_command

from menu import get_start_menu


def start():
    choice = get_start_menu("Welcome to Epic Events")

    if choice == 1:
        call_command("employee")
    if choice == 2:
        call_command("contract")
    if choice == 3:
        call_command("event")


if __name__ == "__main__":
    start()
