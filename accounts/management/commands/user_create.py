from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to create a new user."

    def handle(self, *args, **options):
        while True:
            email = str(input(" Enter the email address: "))
            user = UserModel.objects.filter(email=email).first()
            if user is not None:
                self.stdout.write("  Sorry, this user exists already! \n\n")
                self.stdout.flush()
            else:
                password = str(input(" Please enter the password: "))
                UserModel.objects.create_user(email=email, password=password)
                self.stdout.write()
                self.stdout.write("   A new user was created. \n\n")
                call_command("user")
                break
