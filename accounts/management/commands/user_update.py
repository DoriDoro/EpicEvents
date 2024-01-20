import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Command to update a new user."

    def add_arguments(self, parser):
        parser.add_argument(
            "email",
            type=str,
            help="Email of user.",
        )
        parser.add_argument(
            "--update_data",
            metavar="KEY=VALUE",
            nargs="+",
            type=str,
            help="Either an email address or a password or both.",
        )

    def handle(self, *args, **options):
        dict_arg = options["update_data"]

        # converting the dict_arg/options["update_data"]
        # in a new dictionary dict_obj
        dict_obj = {item.split("=")[0]: item.split("=")[1] for item in dict_arg}

        user = UserModel.objects.get(email=options["email"])

        # check if email or password or both:
        for key, value in dict_obj.items():
            if key == "email":
                user.email = value
            if key == "password":
                # to hash and salt the password
                user.set_password(value)

            user.save()
