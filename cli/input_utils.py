def customer_input(field_name):
    field_name = field_name.title()
    return input(f"  Enter the {field_name}: ")


def customer_int_input(field_name):
    field_name = field_name.title()
    return int(input(f"  Enter the {field_name}: "))
