def customer_input(field_name):
    field_name = field_name.title()
    try:
        input_customer = input(f"  Enter the {field_name}: ")
        return input_customer

    except ValueError:
        print("   Invalid input. Please enter a number. \n")


def customer_int_input(field_name):
    field_name = field_name.title()
    try:
        input_customer = int(input(f"  Enter the {field_name}: "))
        return input_customer

    except ValueError:
        print("   Invalid input. Please enter a number. \n")
