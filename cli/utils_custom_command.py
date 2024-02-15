from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, call_command
from django.core.validators import validate_email
from django.utils.timezone import make_aware

from cli.utils_menu import BOLD, ENDC, style_text_display, BLUE
from cli.utils_messages import (
    create_invalid_error_message,
    create_permission_denied_message,
)
from cli.utils_tables import create_pretty_table
from cli.utils_token_mixin import JWTTokenMixin


class EpicEventsCommand(JWTTokenMixin, BaseCommand):
    help = "Custom BaseCommand"
    action = None
    permissions = None

    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.object = None
        self.update_fields = list()
        self.fields_to_update = list()
        self.available_fields = dict()
        self.update_table = list()

    @classmethod
    def text_input(cls, label, required=True):
        """
        Prompts the user for text/string input and handles required fields.

        This method displays a prompt to the user with a given label and
        optionally marks the field as required. If the field is marked as
        required, the method ensures that the user provides a non-empty
        input. If the user does not provide an input or enters only whitespace,
        the method calls 'start' command and prints a blank line. If the
        field is not required or the user provides a valid input, the method
        returns the input value.

        Args:
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            str: The user's input as a string.

        Raises:
            ValueError: If the input is required but not provided.
        """
        if required:
            label = f"{label}*"
        label = f"{'':^5}{BOLD}{label}{ENDC}: "

        value = input(label)
        if required:
            if value in ["", " "]:
                print()
                call_command("start")

            while not value:
                create_invalid_error_message("input")
                value = input(label)

        return value

    @classmethod
    def int_input(cls, label, required=True):
        """
        Prompts the user for number/int input and handles required fields. Exit of function
        possible with '' or ' '.

        Args:
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            int: The user's input as an int.

        Notes:
            uses a ValueError if the input of user is '', the 'start'-command will be called to
            exit the function.
        """
        if required:
            label = f"{label}*"
        label = f"{'':^5}{BOLD}{label}{ENDC}: "

        try:
            value = int(input(label))
        except ValueError:
            print()
            call_command("start")

        if required:
            while not value:
                print("Invalid input! Number input.")
                value = int(input(label))

        return value

    @classmethod
    def decimal_input(cls, label, required=True):
        """
        Prompts the user for decimal/float input and handles required fields.

        Args:
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            float: The user's input as a decimal/float.

        Raises:
            InvalidOperation: If the input is other than decimal.
        """
        if required:
            label = f"{label}*"
        label = f"{'':^5}{BOLD}{label}{ENDC}: "

        value = input(label)

        if required:
            if value in ["", " "]:
                print()
                call_command("start")

            try:
                value = Decimal(value)
            except InvalidOperation:
                print("Invalid input! Decimal input.")
                value = input(label)

        return value

    @classmethod
    def choice_str_input(cls, options, label, required=True):
        """
        Prompts the user for one choice string input and handles required fields.

        Args:
            options (tuple): The options are the possible choices the user can make.
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            str: The user's input as a string.

        Notes:
            If the user enters '' or ' ' the program calls the 'start'-command to exit.
        """
        value = cls.text_input(label, required)

        if value not in options:
            value = cls.choice_str_input(options, label, required)
        if value in ["", " "]:
            print()
            call_command("start")

        return value

    @classmethod
    def choice_int_input(cls, options, label, required=True):
        """
        Prompts the user for one choice int input and handles required fields.

        Args:
            options (tuple): The options are the possible choices the user can make.
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            int: The user's input as an int.

        Notes:
            If the user enters '' or ' ' the program calls the 'start'-command to exit.
        """
        value = cls.int_input(label, required)

        if value not in options:
            value = cls.choice_int_input(options, label, required)
        if value in ["", " "]:
            print()
            call_command("start")

        return value

    @classmethod
    def multiple_choice_str_input(cls, options, label, required=True):
        """
        Prompts the user for one or many choice(s) as string input(s) and handles required fields.

        Args:
            options (tuple): The options are the possible choices the user can make.
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            list: The user's input as a list.

        Notes:
            If the user enters '' or ' ' the program calls the 'start'-command to exit.
        """
        values = cls.text_input(label, required)

        if values in ["", " "]:
            print()
            call_command("start")

        return [w for w in values if w in options]

    @classmethod
    def date_input(cls, label, required=True):
        """
        Prompts the user for a date input in format: DD/MM/YYYY and handles required fields.

        Args:
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            date: The user's input as a date object.

        Notes:
            If the user enters '' or ' ' the program calls the 'start'-command to exit.
        """
        value = cls.text_input(label, required)  # DD/MM/YYYY

        if value in ["", " "]:
            print()
            call_command("start")

        try:
            # save the given date in format: 2025-12-15 00:00:00
            value = datetime.strptime(value, "%d/%m/%Y")
            # Make the datetime object timezone-aware
            value = make_aware(value)
        except ValueError:
            value = cls.date_input(label, required)

        return value

    @classmethod
    def email_input(cls, label, required=True):
        """
        Prompts the user for a valid email input and handles required fields. The build-in function
        'validate_email' checks if the email input is a valid email address.

        Args:
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            email: The user's input as an email.

        Raises:
            ValidationError: Uses the ValidationError to recall the function again if the email
            address is wrong.

        Notes:
            If the user enters '' or ' ' the program calls the 'start'-command to exit.
        """
        value = cls.text_input(label, required)

        if value in ["", " "]:
            print()
            call_command("start")

        try:
            validate_email(value)
        except ValidationError:
            value = cls.email_input(label, required)

        return value

    @classmethod
    def password_input(cls, label, required=True):
        """
        Prompts the user for a valid password input and handles required fields. The build-in
        function 'validate_password' checks if the password input fits the
        'settings.AUTH_PASSWORD_VALIDATORS'

        Args:
            label (str): The label to display next to the input prompt.
            required (bool, optional): Whether the input field is required. Defaults to True.

        Returns:
            password: The user's input as a password.

        Raises:
            ValidationError: Uses the ValidationError to recall the function again if the password
            does not fit the 'settings.AUTH_PASSWORD_VALIDATORS' criteria and prints the error
            message, why the password is not valid.

        Notes:
            If the user enters '' or ' ' the program calls the 'start'-command to exit.
        """
        value = cls.text_input(label, required)

        if value in ["", " "]:
            print()
            call_command("start")

        try:
            validate_password(value)
        except ValidationError as e:
            print(f"{'':^4}", e.messages)
            value = cls.password_input(label, required)

        return value

    @classmethod
    def display_input_title(cls, text):
        """
        Display a title above the input.

        Args:
             text (str): The text is the printed title above the input.
        """
        style_text_display(f"{'':^3}{text} {'':^3}", color=BLUE, bold=True)

    def display_new_line(self):
        """Prints a new line"""
        print()

    # METHODS FOR ACTION:
    def get_create_model_table(self):
        """Within this method, create a table of the existing model instances."""
        pass

    def get_requested_model(self):
        """
        Prompt the user for the email or other required details to find the corresponding model.
        Displays a or several table(s) with help of 'cli/utils_table.py'.
        """
        pass

    def get_available_fields(self):
        """
        Sets the instance attribute 'available_fields'.

        Returns:
            dict: Contains the 'method', 'params' and 'label' to display in 'get_data' the
            necessary input-types.
        """
        pass

    def get_fields_to_update(self):
        """
        Uses the 'multiple_choice_str_input' to retrieve the user's input. These choices will be
        transmitted to the 'get_data' method to call the necessary inputs. And sets the instance
        attribute 'field_to_update'.

        Returns:
            list: Contains a list of the option(s) which the user entered.
        """
        return self.fields_to_update

    def get_data(self):
        """
        Prompts the user for data/information.

        Returns:
            dict: Gets the user's input and is stored in a dictionary.
        """
        return dict()

    def make_changes(self, data):
        """
        Verifies if the user's input from 'get_data' exists. Makes queries to verify the user's
        input from the database. Makes the changes: 'create', 'update' or 'delete'.

        Args:
             data (dict): Contains the user's input from 'get_data' function.

        Errors:
            Throws different error messages, which are defined in 'cli/utils_messages.py'.
        """
        return None

    def collect_changes(self):
        """
        Collects changes made to the object by iterating over instance attribute 'update_fields'.

        This method constructs the content of the table by iterating through each field
        listed in the 'update_fields' attribute. For each field, it checks if the
        field exists within the 'object' attribute. If the field has a corresponding
        display method (e.g., `get_field_display()`), it uses that method to retrieve
        the display value; otherwise, it retrieves the raw value of the field.
        Field names are formatted to replace underscores with spaces and capitalized
        for presentation. The resulting key-value pairs are appended to the
        'update_table' attribute.

        Notes:
            This method assumes that the 'update_fields' attribute contains a list
            of strings representing the names of fields to be displayed, and that the
            'object' attribute contains an instance of a model with the corresponding fields.
        """
        for field in self.update_fields:
            if hasattr(self.object, field):
                field_item = getattr(self.object, field)

                # Check if the field has choices and get the display value if available
                if hasattr(self.object, f"get_{field}_display"):
                    field_item = getattr(self.object, f"get_{field}_display")()

                field = field.replace("_", " ")
                self.update_table.append([f"{field.capitalize()}: ", field_item])

    def create_table(self):
        """
        Creates a table with help of library: 'tabulate'. It takes the instance attribute
        'update_table' to create the table, 'cli/utils_tables.py'.
        """
        create_pretty_table(self.update_table)

    def go_back(self):
        """Calls another Command."""
        pass

    # METHODS FOR HANDLE:

    def list(self):
        """Methods when action='LIST' in the child Command."""
        self.get_create_model_table()
        self.go_back()

    def create(self):
        """Methods when action='CREATE' in the child Command."""
        self.get_create_model_table()
        validated_data = self.get_data()
        self.make_changes(validated_data)
        self.collect_changes()
        self.create_table()
        self.go_back()

    def update(self):
        """Methods when action='UPDATE' in the child Command."""
        self.get_create_model_table()
        self.get_requested_model()
        self.get_fields_to_update()
        self.get_available_fields()
        validated_data = self.get_data()
        self.make_changes(validated_data)
        self.collect_changes()
        self.create_table()
        self.go_back()

    def delete(self):
        """Methods when action='DELETE' in the child Command."""
        self.get_create_model_table()
        self.get_requested_model()
        validated_data = self.get_data()
        self.make_changes(validated_data)
        self.collect_changes()
        self.go_back()

    def handle(self, *args, **options):
        """
        Handles the execution of the custom command based on the action specified.

        This method first calls the parent class's handle method to perform any
        necessary setup. Then it checks if the current user has the required
        permissions for the specified action. If the user lacks the necessary
        permissions, a permission denied message is displayed and the 'start'
        command is called. If the user has the correct permissions, the method
        dispatches to the appropriate method based on the action: LIST, CREATE,
        UPDATE, or DELETE.
        """
        super().handle(*args, **options)

        if self.user.employee_users.role not in self.permissions:
            create_permission_denied_message()
            call_command("start")
            return

        if self.action == "LIST":
            self.list()
        elif self.action == "CREATE":
            self.create()
        elif self.action == "UPDATE":
            self.update()
        elif self.action == "DELETE":
            self.delete()
