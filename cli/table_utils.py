from tabulate import tabulate

from cli.menu import style_text_display, CYAN


def display_table_title(text):
    style_text_display(f"{'':^3}{text} {'':^3}", color=CYAN, bold=True)


def create_pretty_table(title, table_list):
    display_table_title(title)

    table = tabulate(table_list, tablefmt="pretty")
    indented_table = "\n".join("   " + line for line in table.split("\n"))
    print(indented_table)
    print()
