from django.contrib.auth import get_user_model
from django.core.management import call_command
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
                print(
                    "   This email address is not known. Please enter a valid email address."
                )
            else:
                f_name = str(input(" Please enter the first name: "))
                l_name = str(input(" Please enter the last name: "))

                print("  Choose the role of your employee:")
                print(f"   [1] Sales")
                print(f"   [2] Support")
                print(f"   [3] Management")
                while True:
                    try:
                        role = int(input(" Please enter your choice for the role: "))
                        print(role)
                        break
                    except ValueError:
                        print("   Invalid input. Please enter a number.", end="\n\n")

                employee_exists = Employee.objects.filter(user=user).exists()

                if employee_exists:
                    print()
                    self.stdout.write(
                        f"   This employee: {user} with role: {role} exists already!"
                    )
                    print()
                else:
                    employee = Employee(
                        user=user,
                        first_name=f_name,
                        last_name=l_name,
                        role=role,
                    )
                    employee.save()
                    print()
                    self.stdout.write("   A new employee was created.")
                    break
