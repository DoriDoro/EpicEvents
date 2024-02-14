from tabulate import tabulate

from cli.utils_menu import display_new_line, style_text_display, CYAN
from cli.utils_messages import create_info_message


def display_table_title(text):
    """
    Prints the title of the table with specified styling.

    Args:
        text (str): The title text to be displayed.
    """
    if text is None or text.strip() == "":
        raise ValueError("Title text cannot be empty or None")

    styled_text = f"{'':^3}{text} {'':^3}"  # Center-align the text with padding
    style_text_display(styled_text, color=CYAN, bold=True)


def create_pretty_table(table_list, title=None, headers=None):
    """
    Creates a formatted table using the tabulate library.

    Args:
        table_list (list): List of lists representing the rows of the table.
        title (str, optional): Title to display above the table. Defaults to None.
        headers (list, optional): List of strings representing column headers. Defaults to None.
    """
    if not table_list:
        print("No data available to create table.")
        return

    if title:
        display_table_title(title)

    table_format = "pretty"
    if headers is not None:
        table = tabulate(table_list, headers=headers, tablefmt=table_format)
    else:
        table = tabulate(table_list, tablefmt=table_format)

    indented_table = "\n".join("   " + line for line in table.split("\n"))
    print(indented_table)
    display_new_line()


def create_model_table(model, column_label, title):
    """
    Creates data for the create_pretty_table function based on a model.

    Args:
        model (Model): Django model class.
        column_label (str): Label of the column to display.
        title (str): Title for the table.
    """
    if not hasattr(model, column_label):
        create_info_message(f"Invalid column label: {column_label}")
        return

    all_items = model.objects.all()
    all_items_list = []

    if all_items:
        for item in all_items:
            if "." in column_label:
                # Handle nested attributes
                attribute_chain = column_label.split(".")
                attribute_value = item
                for attr in attribute_chain:
                    attribute_value = getattr(attribute_value, attr)
                column_title = attribute_chain[-1].title()
            else:
                attribute_value = getattr(item, column_label)
                column_title = column_label.title()

            all_items_table = [column_title + ": ", attribute_value]
            all_items_list.append(all_items_table)

        create_pretty_table(all_items_list, f"All {title}: ")
    else:
        create_info_message(f"No {model}-table available, until now!")


def create_queryset_table(queryset, title, label=None, headers=None):
    """
    Creates a formatted table based on the provided queryset, title, label, and headers.

    Args:
        queryset: A Django QuerySet representing the data to be displayed in the table.
        title (str): The title of the table.
        label (str, optional): A label to prepend to each row of the table. Defaults to None.
        headers (list, optional): A list of column headers for the table. If provided, each row
            in the table will be labeled with these headers. Defaults to None.

    Returns:
        None: The function does not return a value. Instead, it prints the formatted table.

    Note:
        The function formats the table based on the provided queryset, title, label, and headers.
        If both label and headers are provided, each row will be labeled with the label, and the
        table will have the specified headers. If only label is provided, each row will be labeled
        with the label. If only headers are provided, the table will have the specified headers.
        If neither label nor headers are provided, the table will display the queryset directly.

        This function assumes that the `create_pretty_table` function is defined elsewhere to
        handle the actual formatting of the table.
    """
    if not queryset:
        create_info_message("No data available!")
        return

    all_items_list = []

    if label is not None:
        for item in queryset.values():
            item_table = [label + ": ", item]
            all_items_list.append(item_table)
        create_pretty_table(all_items_list, f"All {title}: ")

    if headers is not None:
        for key, values in queryset.items():
            item_table = [f"{key}: "]
            for value in values.values():
                item_table.append(value)
            all_items_list.append(item_table)
        create_pretty_table(all_items_list, headers=headers, title=f"All {title}: ")
