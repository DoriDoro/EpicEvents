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
            "update_data",
            type=json.loads,
            help="Either an email address or a password or both.",
        )

    def handle(self, *args, **options):
        update_data_str = options["update_data"]
        try:
            update_data = json.loads(update_data_str)
        except json.JSONDecodeError:
            raise CommandError(f"Invalid JSON: {update_data_str}")

        user = UserModel.objects.get(email=options["email"])

        # check if email or password or both:
        for key, value in options["update_data"]:
            if key == "email":
                user.email = value
            if key == "password":
                # to hash and salt the password
                user.set_password(value)

            user.save()
