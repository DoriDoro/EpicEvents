from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from tabulate import tabulate

from cli.input_utils import customer_input

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

        email_all_users = []

        all_users = UserModel.objects.all()

        for user in all_users:
            all_users_table = ["Email: ", user.email]
            email_all_users.append(all_users_table)

        # display all users
        all_users_table = tabulate(email_all_users, tablefmt="pretty")
        indented_table = "\n".join("   " + line for line in all_users_table.split("\n"))
        self.stdout.write(indented_table)
        self.stdout.write()

        while True:
            email = customer_input("email address")
            self.stdout.write()
            user = UserModel.objects.filter(email=email).first()

            if user is None:
                self.stdout.write("   This email address is unknown. \n\n")

            else:
                # TODO: use menu to get the choice
                self.stdout.write("   Which details you want to update?")
                self.stdout.write("    [1] Email")
                self.stdout.write("    [2] Password")
                self.stdout.write("    [3] go back to User Menu \n\n")

                update_str = input(
                    " Which details you want to update? (several numbers possible): "
                )
                # TODO: control missing to check if user enters min one number
                # update_list is a list with one or more numbers from input of customer
                update_list = [int(num) for num in update_str.split()]

                # go through the dict of choices and verify if number in update_list
                # and keys of user+fields are the same
                for key, field in user_fields.items():
                    for number in update_list:
                        if key == number:
                            update_user_list.append(field)

                # check if the user has chosen 3: 'quit'
                for field in update_user_list:
                    if field == "quit":
                        call_command("user")
                        break
                    else:
                        update_user[field] = customer_input(field)

                # TODO: control missing if update_user is an empty dictionary
                #     probably not necessary because if ENTER ask again for email address
                # in update_user (dictionary) can be an email or a password or both
                if update_user:
                    # when user updates email AND password
                    if len(update_user) == 2:
                        update_user_email = None
                        update_user_password = None

                        for key, field in update_user.items():
                            if key == "email":
                                update_user_email = field
                            elif key == "password":
                                update_user_password = field

                        if (
                            update_user_email is not None
                            and update_user_password is not None
                        ):
                            # user_update expects a KEY=VALUE pair, create a variable and
                            # assign the key=value
                            update_data = f"email={update_user_email},password={update_user_password}"

                            call_command(
                                "user_update",
                                email,
                                "--update_data",
                                update_data,
                            )

                    # when user update just the email OR the password
                    if len(update_user) == 1:
                        for key, field in update_user.items():
                            if key == "email":
                                update_data_email = f"email={field}"
                                call_command(
                                    "user_update",
                                    email,
                                    "--update_data",
                                    update_data_email,
                                )
                            if key == "password":
                                update_data_password = f"password={field}"
                                call_command(
                                    "user_update",
                                    email,
                                    "--update_data",
                                    update_data_password,
                                )

                    self.stdout.write("\n  The user was updated. \n\n")
                    self.stdout.write("  Updated data of the user:")

                    display_password = "*" * 10
                    table = [
                        ["Email:", update_user["email"]],
                        ["Password:", display_password],
                    ]
                    table = tabulate(table, tablefmt="pretty")
                    indented_table = "\n".join(
                        "   " + line for line in table.split("\n")
                    )
                    self.stdout.write(indented_table)

                    call_command("user")
                    break
