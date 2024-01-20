from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tabulate import tabulate

from accounts.models import Employee
from cli.input_utils import customer_input, customer_int_input
from cli.menu_utils import create_menu
from cli.table_utils import create_pretty_table

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to update a employee."

    def handle(self, *args, **options):
        email_all_users = []

        updates = {}

        all_employees = Employee.objects.all()

        for employee in all_employees:
            all_employees_table = ["Email: ", employee.user.email]
            email_all_users.append(all_employees_table)

        # display all users
        create_pretty_table("All employees:", email_all_users)

        while True:
            email = customer_input("email address")
            self.stdout.write()

            employee = Employee.objects.filter(user__email=email).first()

            if employee is None:
                self.stdout.write("   This email address is unknown. \n\n")

            else:
                employee_table = [
                    ["Email: ", employee.user.email],
                    ["First Name: ", employee.first_name],
                    ["Last Name: ", employee.last_name],
                    ["Role: ", employee.role],
                ]

                create_pretty_table(
                    "Here are all information about this employee:", employee_table
                )

                while True:
                    update_first_name = input(
                        " Do you want to update the first name? (yes/no): "
                    ).lower()
                    if update_first_name not in ["yes", "y", "no", "n"]:
                        self.stdout.write("Invalid answer. \n\n")
                    if update_first_name in ["no", "n"]:
                        break
                    if update_first_name in ["yes", "y"]:
                        f_name = customer_input("first name")
                        updates["first_name"] = f_name
                        break

                while True:
                    update_last_name = input(
                        " Do you want to update the last name? (yes/no): "
                    ).lower()
                    if update_last_name not in ["yes", "y", "no", "n"]:
                        self.stdout.write("Invalid answer. \n\n")
                    if update_last_name in ["no", "n"]:
                        break
                    if update_last_name in ["yes", "y"]:
                        l_name = customer_input("last name")
                        updates["last_name"] = l_name
                        break

                while True:
                    """
                    Do you want to update the role? (yes/no): y
                      Choose the role of your employee:
                       [1] Sales
                       [2] Support
                       [3] Management

                     Enter the Role: 2
                    Do you want to update the role? (yes/no): n
                    """
                    update_role = input(
                        " Do you want to update the role? (yes/no): "
                    ).lower()
                    if update_role not in ["yes", "y", "no", "n"]:
                        self.stdout.write("Invalid answer. \n\n")
                    if update_role in ["no", "n"]:
                        break
                    if update_role in ["yes", "y"]:
                        choices = {1: "Sales", 2: "Support", 3: "Management"}
                        create_menu("Choose the role of your employee: ", choices)

                        while True:
                            get_role = {1: "Sales", 2: "Support", 3: "Management"}

                            role_number = customer_int_input("role")
                            if role_number in get_role:
                                updates["role"] = get_role[role_number]
                                break
                            else:
                                self.stdout.write(
                                    "Invalid role number. "
                                    "Please enter a number between 1 and 3. \n\n"
                                )

            if updates:
                # Employee.objects.filter(user=employee.user).update(**updates)
                self.stdout.write()
                updated_employee_table = []

                for key, value in updates.items():
                    if key == "first_name":
                        updated_employee_table.append(["First Name: ", value])
                    if key == "last_name":
                        updated_employee_table.append(["Last Name: ", value])
                    if key == "role":
                        updated_employee_table.append(["Role: ", value])

                create_pretty_table(
                    "Here are all information about this employee:",
                    updated_employee_table,
                )

                self.stdout.write("  The employee was updated. \n\n")
                break
            else:
                self.stdout.write("  No changes made. \n\n")
                break
