from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Employee

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Command to update a new employee."

    def add_arguments(self, parser):
        parser.add_argument(
            "--update_data",
            metavar="KEY=VALUE",
            nargs="+",
            type=str,
            help="Either an email address or a password or both.",
        )

    def handle(self, *args, **options):
        dict_arg = options["update_data"]

        # get the string from the list
        dict_str = dict_arg[0]

        # Split the string into separate key-value pairs
        dict_pairs = dict_str.split(", ")

        # create a new dictionary with key:value pairs
        dict_obj = {pair.split("=")[0]: pair.split("=")[1] for pair in dict_pairs}

        user = UserModel.objects.get(email=dict_obj["user"])

        employee = Employee(
            user=user,
            first_name=dict_obj["first_name"],
            last_name=dict_obj["last_name"],
            role=dict_obj["role"],
        )
        employee.save()
