BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

BOLD = "\033[1m"
UNDERLINE = "\033[4m"

ENDC = "\033[0m"


def style_text_display(
    text, color=ENDC, background=None, bold=False, underline=False, end="\n"
):
    style = f"{color}"
    if bold:
        style += f"{BOLD}"
    if underline:
        style += f"{UNDERLINE}"
    if background:
        style += f"{background}"
    print(f"{style}{text}{ENDC}", end=end)  # {ENDC} resets the color


def _display_menu_headline(text):
    style_text_display(
        f"{'':^2}** {text} **{'':^2}",
        color=MAGENTA,
        bold=True,
        underline=True,
        end="\n\n",
    )


def _display_menu_title(text):
    style_text_display(f"{'':^3}*** {text} ***{'':^3}", color=CYAN, bold=True)


def display_choices(option, text, color=BLUE):
    """choice is [1] Manage the ..."""
    style_text_display(f"{'':^4}[{option}] ", color=color, bold=True, end="")
    style_text_display(f"{text}", bold=True)


def display_new_line():
    print()


def get_start_menu(title):
    possible_choices = {
        1: "employees",
        2: "clients",
        3: "contracts",
        4: "events",
        5: "quit",
        6: "logout",
    }

    title_headline = f"Welcome to {title}"
    text_title = f"{title} Menu"

    _display_menu_headline(title_headline)

    _display_menu_title(text_title)

    for key, choice in possible_choices.items():
        if choice == "quit":
            display_choices(key, "Quit program", color=RED)
        if choice == "logout":
            display_choices(key, "Logout", color=RED)
            display_new_line()
        if choice in ["employees", "clients", "contracts", "events"]:
            display_choices(key, f"Manage the {choice}")

    while True:
        try:
            choice = int(input(" Please enter your choice: "))
            print()
            break
        except ValueError:
            print("   Invalid input. Please enter a number.", end="\n\n")

    return choice


def get_app_menu(app):
    possible_choices = {
        1: "Create",
        2: "Update",
        3: "Delete",
        4: "quit",
    }
    app_capitalized = app.title()

    _display_menu_headline(f"Menu of the {app_capitalized}s")

    _display_menu_title(f"{app_capitalized} Menu")

    for key, choice in possible_choices.items():
        if choice == "quit":
            display_choices(key, "Go back to Main Menu", color=RED)
            display_new_line()
        else:
            display_choices(key, f"{choice} an {app}")

    while True:
        try:
            choice = int(input(" Please enter your choice: "))
            print()
            break
        except ValueError:
            print("   Invalid input. Please enter a number.", end="\n\n")

    return choice
