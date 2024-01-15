from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Employee

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Creates a new employee."

    def handle(self, *args, **options):
        while True:
            email = str(
                input(" Please enter the email address of the future employee: ")
            )
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                self.stdout.write(
                    "   This email address is not known. Please enter a valid email address. \n\n"
                )
                self.stdout.flush()
            else:
                f_name = str(input(" Please enter the first name: "))
                l_name = str(input(" Please enter the last name: "))

                self.stdout.write(" Choose the role of your employee:")
                self.stdout.write(f"  [1] Sales")
                self.stdout.write(f"  [2] Support")
                self.stdout.write(f"  [3] Management")
                self.stdout.flush()

                while True:
                    get_role = {1: "Sales", 2: "Support", 3: "Management"}
                    try:
                        role_number = int(
                            input("  Please enter your choice for the role: ")
                        )
                        if role_number in get_role:
                            role = get_role[role_number]
                            break
                        else:
                            self.stdout.write(
                                "Invalid role number. Please enter a number between 1 and 3. \n\n"
                            )
                            self.stdout.flush()
                    except ValueError:
                        self.stdout.write(
                            "   Invalid input. Please enter a number. \n\n"
                        )
                        self.stdout.flush()

                employee_exists = Employee.objects.filter(user=user).first()

                if employee_exists:
                    self.stdout.write(
                        f"   This employee: {user.email} with role: "
                        f"{employee_exists.role} exists already! "
                        f"Please choose an other email address to create an employee. \n\n"
                    )
                    self.stdout.flush()
                else:
                    employee = Employee(
                        user=user,
                        first_name=f_name,
                        last_name=l_name,
                        role=role,
                    )
                    employee.save()
                    self.stdout.write()
                    self.stdout.write("   A new employee was created. \n\n")
                    break
