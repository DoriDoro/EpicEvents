from cli.menu import style_text_display, YELLOW, RED


def create_success_message(text, action):
    style_text_display(f" {text} successfully {action}!", color=YELLOW)
    print()


def create_error_message(text):
    style_text_display(f"{'':^2}{text} exists already !", color=RED, bold=True)
    print()
