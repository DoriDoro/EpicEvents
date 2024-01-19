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

        while True:
            all_users = UserModel.objects.all()

            for user in all_users:
                user_table = ["Email: ", user.email]
                email_all_users.append(user_table)

            user_table = tabulate(email_all_users, tablefmt="pretty")
            indented_table = "\n".join("   " + line for line in user_table.split("\n"))
            self.stdout.write(indented_table)
            self.stdout.write()

            email = customer_input("email address")
            user = UserModel.objects.filter(email=email).first()

            if user is None:
                self.stdout.write("   This email address is unknown. \n\n")

                """
                  Enter Email Address: kjo#mail.com
                   This email address is unknown. 
                
                   +--------+----------------+
                   | Email: |   m@mail.com   |
                   | Email: | test@mail.com  |
                   | Email: | supp@mail.com  |
                   | Email: | sales@mail.com |
                   | Email: |  man@mail.com  |
                   | Email: |  Kjo#mail.com  |
                   | Email: |   m@mail.com   |
                   | Email: | test@mail.com  |
                   | Email: | supp@mail.com  |
                   | Email: | sales@mail.com |
                   | Email: |  man@mail.com  |
                   | Email: |  Kjo#mail.com  |
                   +--------+----------------+

                """
            else:
                self.stdout.write("   All information about this user:")
                display_password = "*" * 10
                table = [["Email:", email], ["Password:", display_password]]
                table = tabulate(table, tablefmt="pretty")
                indented_table = "\n".join("   " + line for line in table.split("\n"))
                self.stdout.write(indented_table)

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

                print(update_user)

                # TODO: control missing if update_user is an empty dictionary
                #     probably not necessary because if ENTER ask again for email address
                # in update_user (dictionary) can be an email or a password or both
                if update_user:
                    call_command("user_update", email, update_user)
                    # this command is not working with one values
                    """
                    File "/home/doro/Desktop/DR_P12/P12/EpicEvents/accounts/management/
                    commands/user_update.py", line 26, in handle
                    for key, value in options["update_data"]:
                    ^^^^^^^^^^
                    ValueError: not enough values to unpack (expected 2, got 1)

                    """

                    self.stdout.write("\n  The user was updated. \n\n")
                    self.stdout.write("  Updated data of the user:")
                    # TODO: table
                    display_password = "*" * 10
                    table = [["Email:", email], ["Password:", display_password]]
                    table = tabulate(table, tablefmt="pretty")
                    indented_table = "\n".join(
                        "   " + line for line in table.split("\n")
                    )
                    self.stdout.write(indented_table)

                    call_command("user")
                    break
