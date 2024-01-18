from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to update a user."

    def handle(self, *args, **options):
        update_user = {}

        user_fields = {
            1: "email",
            2: "password",
            3: "quit",
        }

        update_user_list = []

        while True:
            email = input(" Enter the email address: ")
            user = UserModel.objects.filter(email=email).first()

            if user is None:
                self.stdout.write("   This email address is unknown. \n\n")
            else:
                # TODO: use a table to display this info
                self.stdout.write("   All information about this user:")
                self.stdout.write(f"    Email: {email}")
                self.stdout.write(f"    Password: {'*' * 10} \n\n")

                # TODO: use a table to display this info
                self.stdout.write("   Which details you want to update?")
                self.stdout.write("    [1] Email")
                self.stdout.write("    [2] Password")
                self.stdout.write("    [3] go back to User Menu \n\n")

                update_str = input(
                    " Which details you want to update? (several numbers possible): "
                )
                # TODO: control missing to check if user enters min one number
                update_list = [int(num) for num in update_str.split()]

                for key, field in user_fields.items():
                    for number in update_list:
                        if key == number:
                            update_user_list.append(field)

                for field in update_user_list:
                    if field == "quit":
                        call_command("user")
                        break
                    else:
                        update_user[field] = input(f"  Please enter the new {field}: ")

                # TODO: control missing if update_user is an empty dictionary
                #     probably not necessary because if ENTER ask again for email address
                if update_user:
                    user_to_update = UserModel.objects.get(email=email)

                    for field in update_user:
                        if field == "email":
                            user_to_update.email = update_user["email"]
                        if field == "password":
                            # to hash and salt the password
                            user_to_update.set_password(update_user["password"])
                    user_to_update.save()

                    self.stdout.write("\n  The user was updated. \n\n")
                    self.stdout.write("  Updated data of the user:")
                    self.stdout.write(f"   Email: {user_to_update.email}")
                    self.stdout.write(f"   Password: {'*' * 10} \n\n")

                    call_command("user")
                    break
