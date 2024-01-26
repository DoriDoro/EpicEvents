from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.core.validators import validate_email

from cli.menu import BOLD, ENDC


class EpicEventsCommand(BaseCommand):
    help = "Custom BaseCommand"
    action = None

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
        """handles one to many choices as string/text input"""
        value = cls.text_input(label, required)

        if value not in options:
            value = cls.choice_str_input(options, label, required)

        return value

    @classmethod
    def choice_int_input(cls, options, label, required=True):
        """handles one to many choices as int input"""
        value = cls.number_input(label, required)

        if value not in options:
            value = cls.choice_int_input(options, label, required)

        return value

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

    def get_data(self):
        """all data to make_changes"""
        return dict()

    def make_changes(self, data):
        return None

    def display_changes(self, instance):
        pass

    def go_back(self):
        pass

    def create(self):
        self.get_create_model_table()
        validated_data = self.get_data()
        instance = self.make_changes(validated_data)
        self.display_changes(instance)
        self.go_back()

    def handle(self, *args, **options):
        if self.action == "CREATE":
            self.create()

        # elif self.action == "UPDATE":
        #     self.update()
        # elif self.action == "DELETE":
        #     self.delete()

    # def create_pretty_table(self, title, table_list):
    #     style_text_display(f"{'':^3}{title} {'':^3}", color=CYAN, bold=True)
    #
    #     table = tabulate(table_list, tablefmt="pretty")
    #     indented_table = "\n".join("   " + line for line in table.split("\n"))
    #     print(indented_table)
    #     print()
