from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Delete a user."

    def handle(self, *args, **options):
        while True:
            email = input(" Please enter the email address to delete the user: ")
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                self.stdout.write(
                    "   This email address is not known. Please enter a valid email address. \n\n"
                )
            else:
                try:
                    delete_user = input(
                        f"  Do you want to delete this user {user.email}? (yes/no): "
                    ).lower()

                    if delete_user in ["yes", "y"]:
                        user.delete()
                        self.stdout.write(f" The user {email} was deleted!")
                        break
                    if delete_user in ["no", "n"]:
                        possible_exit = input(
                            "   Do you want to delete an other user (yes) "
                            "or do you want to go back to the main menu? (*): "
                        )
                        if possible_exit == "*":
                            call_command("start")
                            break
                except ValueError:
                    self.stdout.write("Invalid input.")
