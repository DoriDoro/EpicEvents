from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Update a user."

    def handle(self, *args, **options):
        while True:
            email = str(input(" Please enter the email address to update the user: "))
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                self.stdout.write(
                    "   This email address is not known. Please enter a valid email address. \n\n"
                )
            else:
                self.stdout.write("   Here are all information about this user:")
                self.stdout.write(f"    Email: {user.email}")
                self.stdout.write(f"    Password: {'*' * 10} \n\n")

                updates = {}
                update_email = str(
                    input(" Do you want to update the email address? (yes/no): ")
                )
                if update_email.lower() == "yes" or update_email.lower() == "y":
                    new_email = str(input("  Please enter the new email address: "))
                    updates["new_email"] = new_email

                update_password = input(
                    " Do you want to update the password? (yes/no): "
                )
                if update_password.lower() == "yes" or update_password.lower() == "y":
                    new_password = str(input("Please enter the new password: "))
                    user = UserModel.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()
                    self.stdout.write("   The password was changed! \n\n")

                if updates:
                    UserModel.objects.filter(email=email).update(email=new_email)

                    self.stdout.write("  Display the data of the user:")
                    self.stdout.write(f"   Email: {user.email}")
                    self.stdout.write(f"   Password: {'*' * 10} \n\n")
                    self.stdout.write("  The user was updated. \n\n")
                    break
