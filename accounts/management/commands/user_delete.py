from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to delete a user."

    def handle(self, *args, **options):
        while True:
            email = input(" Enter the email address: ")
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                self.stdout.write("   This email address is unknown. \n\n")
            else:
                delete_user = input(
                    f"  Do you want to delete this user {user.email}? (yes/no): "
                ).lower()

                if delete_user not in ["yes", "y", "no", "n"]:
                    self.stdout.write("   Invalid input.")

                if delete_user in ["yes", "y"]:
                    user.delete()
                    self.stdout.write(f" The user {email} was deleted!")
                    break
                if delete_user in ["no", "n"]:
                    possible_exit = input(
                        "   Do you want to delete another user (yes) "
                        "or do you want to go back to the main menu? (*): "
                    )
                    if possible_exit == "*":
                        call_command("start")
                        break
