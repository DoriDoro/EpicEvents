def get_start_menu(title):
    print(f"** {title} **", end="\n\n")

    print(" *** Main Menu *** ")
    print("  [1] Manage the employees")
    print("  [2] Manage the contracts")
    print("  [3] Manage the events")
    print("  [4] Quit program", end="\n\n")

    while True:
        try:
            choice = int(input(" Please enter your choice: "))
            print()
            break
        except ValueError:
            print("   Invalid input. Please enter a number.", end="\n\n")

    return choice


def get_app_menu(app):
    print(f"** Menu of the {app}s **", end="\n\n")

    app_capitalized = app.title()
    print(f" *** {app_capitalized} Menu *** ")
    print(f"  [1] Create an {app}")
    print(f"  [2] Update an {app}")
    print(f"  [3] Delete an {app}")
    print(f"  [4] go back to Main Menu", end="\n\n")

    while True:
        try:
            choice = int(input(" Please enter your choice: "))
            print()
            break
        except ValueError:
            print("   Invalid input. Please enter a number.", end="\n\n")

    return choice
