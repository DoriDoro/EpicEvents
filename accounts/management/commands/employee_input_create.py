from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import Employee
from cli.input_utils import customer_input, customer_int_input

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Prompts for details to crate a new employee."

    def handle(self, *args, **options):
        employee_fields = {
            1: "first_name",
            2: "last_name",
            3: "quit",
        }

        update_employee = {}

        while True:
            email = customer_input("email address")
            user = UserModel.objects.filter(email=email).first()
            update_employee["user"] = user

            if user is None:
                self.stdout.write("   This email address is unknown. \n\n")
            else:
                for value in employee_fields.values():
                    if value == "first_name":
                        update_employee["f_name"] = customer_input("first name")
                    if value == "last_name":
                        update_employee["l_name"] = customer_input("last name")

                # TODO: use menu to get the choice
                #   or add this to employee_fields?
                self.stdout.write()
                self.stdout.write(" Choose the role of your employee:")
                self.stdout.write(f"  [1] Sales")
                self.stdout.write(f"  [2] Support")
                self.stdout.write(f"  [3] Management")

                while True:
                    get_role = {1: "Sales", 2: "Support", 3: "Management"}

                    role_number = customer_int_input("role")

                    if role_number in get_role:
                        update_employee["role"] = get_role[role_number]
                        break
                    else:
                        self.stdout.write(
                            "Invalid role number. Please enter a number between 1 and 3. \n\n"
                        )

            employee_exists = Employee.objects.filter(user=user).first()

            if employee_exists:
                self.stdout.write(
                    f"   This employee: {user.email} with role: "
                    f"{employee_exists.role} exists already! "
                    f"Please choose an other email address to create an employee. \n\n"
                )
            else:
                update_data = (
                    f"user={user}, "
                    f"first_name={update_employee['f_name']}, "
                    f"last_name={update_employee['l_name']}, "
                    f"role={update_employee['role']}"
                )
                call_command("employee_create", "--update_data", update_data)
                self.stdout.write()
                self.stdout.write("   A new employee was created. \n\n")
                call_command("employee")
                break
