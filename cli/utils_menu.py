from cli.menu import (
    style_text_display,
    CYAN,
    RED,
    display_choices,
    display_new_line,
)


def display_choices_title(text):
    style_text_display(f"{'':^3}{text} {'':^3}", color=CYAN, bold=True)


def create_options_menu(title, choices):
    display_choices_title(title)

    for key, choice in choices.items():
        if choice == "quit":
            display_choices(key, "go back", color=RED)
            display_new_line()
        else:
            display_choices(key, f"{choice}")
    display_new_line()
