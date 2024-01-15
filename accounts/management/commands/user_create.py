from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Creates a new user."

    def handle(self, *args, **options):
        while True:
            email = str(input(" Please enter the email address: "))
            user = UserModel.objects.filter(email=email).first()
            if user is not None:
                print("  Sorry, this user exists already!", end="\n\n")
            else:
                password = str(input(" Please enter the password: "))
                UserModel.objects.create_user(email=email, password=password)

                self.stdout.write("   A new user was created.")
                break
