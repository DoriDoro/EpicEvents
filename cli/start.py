from django.core.management import call_command


def get_start_menu(title):
    print(f"** {title} **", end="\n\n")

    print(" *** Main Menu *** ")
    print("  [1] Manage the account managers")
    print("  [2] Manage the contracts")
    print("  [3] Manage the events")
    print("  [4] Quit program", end="\n\n")
    choice = int(input("Please enter your choice: "))
    print(choice)
    print()

    return choice


def start():
    choice = get_start_menu("Welcome to Epic Events")

    if choice == 1:
        call_command("account_manager")
    if choice == 2:
        call_command("contract")
    if choice == 3:
        call_command("event")


if __name__ == "__main__":
    start()
