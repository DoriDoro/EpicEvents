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

    object = None
    update_fields = None
    fields_to_update = None
    available_fields = None
    update_table = None

    @classmethod
    def text_input(cls, label, required=True):
        """handles text/string input"""
        if required:
            label = f"{label}*"
        label = f"{'':^5}{BOLD}{label}{ENDC}: "

        value = input(label)
        if required:
            if value in ["", " "]:
                call_command("start")
                print()
            while not value:
                create_invalid_error_message("input")
                value = input(label)

        return value

    @classmethod
    def int_input(cls, label, required=True):
        """handles number/int input"""
        if required:
            label = f"{label}*"
        label = f"{'':^5}{BOLD}{label}{ENDC}: "

        value = int(input(label))
        if required:
            while not value:
                print("Invalid input! Number input.")
                value = int(input(label))

        return value

    @classmethod
    def decimal_input(cls, label, required=True):
        """handles number/int input"""
        if required:
            label = f"{label}*"
        label = f"{'':^5}{BOLD}{label}{ENDC}: "

        value = input(label)

        if required:
            try:
                value = Decimal(value)
            except InvalidOperation:
                print("Invalid input! Decimal input.")
                value = input(label)

        return value

    @classmethod
    def choice_str_input(cls, options, label, required=True):
        """handles one choice as string/text input"""
        value = cls.text_input(label, required)

        if value not in options:
            value = cls.choice_str_input(options, label, required)

        return value

    @classmethod
    def choice_int_input(cls, options, label, required=True):
        """handles one choice as int input"""
        value = cls.int_input(label, required)

        if value not in options:
            value = cls.choice_int_input(options, label, required)

        return value

    @classmethod
    def date_input(cls, label, required=True):
        """excepts a date with format: DD/MM/YYYY as valid"""
        value = cls.text_input(label, required)  # DD/MM/YYYY

        try:
            # save the given date in format: 2025-12-15 00:00:00
            value = datetime.strptime(value, "%d/%m/%Y")
            # Make the datetime object timezone-aware
            value = make_aware(value)
        except ValueError:
            value = cls.date_input(label, required)

        return value

    @classmethod
    def multiple_choice_str_input(cls, options, label, required=True):
        """handles one to many choices as string/text input"""
        values = cls.text_input(label, required)

        return [w for w in values if w in options]

    @classmethod
    def email_input(cls, label, required=True):
        """checks input if valid email address"""
        value = cls.text_input(label, required)

        try:
            validate_email(value)
        except ValidationError:
            value = cls.email_input(label, required)

        return value

    @classmethod
    def password_input(cls, label, required=True):
        """checks if password is valid (settings.AUTH_PASSWORD_VALIDATORS)"""
        value = cls.text_input(label, required)

        try:
            validate_password(value)
        except ValidationError as e:
            print(f"{'':^4}", e.messages)
            value = cls.password_input(label, required)

        return value

    @classmethod
    def display_input_title(cls, text):
        style_text_display(f"{'':^3}{text} {'':^3}", color=BLUE, bold=True)

    def display_new_line(self):
        print()

    # METHODS FOR ACTION:
    def get_create_model_table(self):
        pass

    def get_requested_model(self):
        """prompt user for the email or ... to find corresponding model"""
        pass

    def get_available_fields(self):
        pass

    def get_fields_to_update(self):
        return self.fields_to_update

    def get_data(self):
        """all data to make_changes"""
        return dict()

    def make_changes(self, data):
        return None

    def display_changes(self):
        for field in self.update_fields:
            if hasattr(self.object, field):
                field_item = getattr(self.object, field)

                # Check if the field has choices and get the display value if available
                if hasattr(self.object, f"get_{field}_display"):
                    field_item = getattr(self.object, f"get_{field}_display")()

                field = field.replace("_", " ")
                self.update_table.append([f"{field.capitalize()}: ", field_item])

    def create_table(self):
        create_pretty_table(self.update_table)

    def go_back(self):
        pass

    # METHODS FOR HANDLE:

    def list(self):
        self.get_create_model_table()
        self.go_back()

    def create(self):
        self.get_create_model_table()
        validated_data = self.get_data()
        self.make_changes(validated_data)
        self.display_changes()
        self.create_table()
        self.go_back()

    def update(self):
        self.get_create_model_table()
        self.get_requested_model()
        self.get_fields_to_update()
        self.get_available_fields()
        validated_data = self.get_data()
        self.make_changes(validated_data)
        self.display_changes()
        self.create_table()
        self.go_back()

    def delete(self):
        self.get_create_model_table()
        self.get_requested_model()
        validated_data = self.get_data()
        self.make_changes(validated_data)
        self.display_changes()
        self.go_back()

    def handle(self, *args, **options):
        super().handle(*args, **options)

        if self.user.employee_users.role not in self.permissions:
            create_permission_denied_message()
            return

        if self.action == "LIST":
            self.list()
        elif self.action == "CREATE":
            self.create()
        elif self.action == "UPDATE":
            self.update()
        elif self.action == "DELETE":
            self.delete()
