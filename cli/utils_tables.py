from tabulate import tabulate

from cli.menu import display_new_line, style_text_display, CYAN


def display_table_title(text):
    style_text_display(f"{'':^3}{text} {'':^3}", color=CYAN, bold=True)


def create_pretty_table(title, table_list):
    display_table_title(title)

    table = tabulate(table_list, tablefmt="pretty")
    indented_table = "\n".join("   " + line for line in table.split("\n"))
    print(indented_table)
    display_new_line()


def contains_period(input_string):
    """used to verify if a parameter contains a '.' like `user.email`"""
    return "." in input_string


def create_model_table(model, column_label, title):
    # for parameter like: user.email
    check_period = contains_period(column_label)

    all_items = model.objects.all()
    all_items_list = list()

    if all_items:
        for item in all_items:
            if check_period:
                split_label = column_label.split(".")  # ['user', 'email']
                attribute = item
                for attr in split_label:
                    attribute = getattr(attribute, attr)
                all_items_table = [(split_label[-1].title()) + ": ", attribute]
                all_items_list.append(all_items_table)

            else:
                all_items_period_table = [
                    (column_label.title()) + ": ",
                    getattr(item, column_label),
                ]
                all_items_list.append(all_items_period_table)

        create_pretty_table(f"All {title}: ", all_items_list)


def create_result_table(model, title):
    new_employee = [
        ["First name:", model.first_name],
        ["Last name:", model.last_name],
        ["Role: ", model.role],
    ]
    create_pretty_table(title, new_employee)
