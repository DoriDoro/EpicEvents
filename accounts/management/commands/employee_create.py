from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import Employee

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Creates a new employee."

    def handle(self, *args, **options):
        email = str(
            input("Please enter the email address of the future employee: ")
        )  # search for the email address of user
        user = UserModel.objects.filter(email=email).first()
        if user is None:
            print(
                "This email address is not known. Please enter a valid email address."
            )  # improve this logic, implement while loop AND quit the program
            while True:
                try:
                    choice = int(input(" Please enter your choice: "))
                    print(choice)
                    print()
                    break
                except ValueError:
                    print("   Invalid input. Please enter a number.", end="\n\n")

        f_name = str(input("Please enter the first name: "))
        l_name = str(input("Please enter the last name: "))
        role = str(
            input("Please enter the role: ")
        )  # improve to make a choice between possible roles
        # while loop until new employee is created
        user_id = options["user"]
        user = UserModel.objects.filter(pk=user_id).first()
        # search for employee with role to verify their existence
        employee_exists = Employee.objects.filter(user=user).exists()

        if employee_exists:
            print()
            self.stdout.write(
                f"This employee: {user} with role: {options['role']} exists already!"
            )
            print()
            call_command("start")

        employee = Employee(
            user=user,
            first_name=options["first_name"],
            last_name=options["last_name"],
            role=options["role"],
        )
        employee.save()

        self.stdout.write("New employee was created.")
