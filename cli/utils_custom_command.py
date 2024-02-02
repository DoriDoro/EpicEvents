from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.core.validators import validate_email

from cli.menu import BOLD, ENDC
from cli.utils_tables import create_pretty_table


class EpicEventsCommand(BaseCommand):
    help = "Custom BaseCommand"
    action = None
    object = None

    update_fields = None
    fields_to_update = None
    available_fields = None

    @classmethod
    def text_input(cls, label, required=True):
        """handles text/string input"""
        if required:
            label = f"{label}*"
        label = f"   {BOLD}{label}{ENDC}: "

        value = input(label)
        if required:
            while not value:
                print("Invalid input!")
                value = input(label)

        return value

    @classmethod
    def number_input(cls, label, required=True):
        """handles number/int input"""
        if required:
            label = f"{label}*"
        label = f"   {BOLD}{label}{ENDC}: "

        value = int(input(label))
        if required:
            while not value:
                print("Invalid input! Number input.")
                value = int(input(label))

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
        value = cls.number_input(label, required)

        if value not in options:
            value = cls.choice_int_input(options, label, required)

        return value

    @classmethod
    def multiple_choice_str_input(cls, options, label, required=True):
        """handles one to many choices as string/text input"""
        values = cls.text_input(label, required)

        return [w for w in values if w in options]
        # for value in values:
        #     if value in options:
        #         check_options.append(value)

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
    def display_new_line(cls):
        print()

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

    def display_changes(self, instance):
        update_table = []
        for field in self.update_fields:
            if hasattr(instance, field):
                field_item = getattr(instance, field)
                field = field.replace("_", " ")
                update_table.append([f"{field.capitalize()}: ", field_item])

        create_pretty_table(update_table)

    def go_back(self):
        pass

    def create(self):
        self.get_create_model_table()
        validated_data = self.get_data()
        instance = self.make_changes(validated_data)
        self.display_changes(instance)
        self.go_back()

    def update(self):
        self.get_create_model_table()
        self.get_requested_model()
        self.get_fields_to_update()
        self.get_available_fields()
        validated_data = self.get_data()

        instance = self.make_changes(validated_data)
        # self.display_changes(instance)
        # self.go_back()

    def handle(self, *args, **options):
        if self.action == "CREATE":
            self.create()
        elif self.action == "UPDATE":
            self.update()

        # elif self.action == "DELETE":
        #     self.delete()
