from cli.utils_menu import style_text_display, YELLOW, RED, GREEN


def create_success_message(text, action):
    print()
    style_text_display(f" {text} successfully {action}!", color=YELLOW)
    print()


def create_error_message(text):
    print()
    style_text_display(f"{'':^2}{text} exists already !", color=RED, bold=True)
    print()


def create_invalid_error_message(text):
    print()
    style_text_display(f"{'':^2} Invalid {text} !", color=RED, bold=True)
    print()


def create_expired_error_message(text):
    print()
    style_text_display(f"{'':^2} {text} expired !", color=RED, bold=True)
    print()


def create_does_not_exists_message(text):
    print()
    style_text_display(f"{'':^2} {text} does not exists !", color=RED, bold=True)
    print()


def create_permission_denied_message():
    print()
    style_text_display(f"{'':^2} Permission denied !", color=RED, bold=True)
    print()


def create_info_message(text):
    print()
    style_text_display(f"{'':^2}{text}", color=GREEN, bold=True)
    print()
