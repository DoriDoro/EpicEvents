from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Employee

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Update a new employee."

    def handle(self, *args, **options):
        while True:
            email = str(
                input(" Please enter the email address to update the employee: ")
            )
            employee = Employee.objects.filter(user__email=email).first()
            if employee is None:
                self.stdout.write(
                    "   This email address is not known. Please enter a valid email address. \n\n"
                )
            else:
                self.stdout.write("   Here are all information about this employee:")
                self.stdout.write(f"    Email: {employee.user.email}")
                self.stdout.write(f"    First name: {employee.first_name}")
                self.stdout.write(f"    Last name: {employee.last_name}")
                self.stdout.write(f"    Role: {employee.role} \n\n")

                updates = {}
                update_first_name = input(
                    " Do you want to update the first name? (yes/no): "
                )
                if (
                    update_first_name.lower() == "yes"
                    or update_first_name.lower() == "y"
                ):
                    f_name = str(input("  Please enter the new first name: "))
                    updates["first_name"] = f_name

                update_last_name = input(
                    " Do you want to update the last name? (yes/no): "
                )
                if update_last_name.lower() == "yes" or update_last_name.lower() == "y":
                    l_name = str(input("  Please enter the new last name: "))
                    updates["last_name"] = l_name

                update_role = input(" Do you want to update the role? (yes/no): ")
                if update_role.lower() == "yes" or update_role.lower() == "y":
                    self.stdout.write("  Choose the role of your employee:")
                    self.stdout.write(f"   [1] Sales")
                    self.stdout.write(f"   [2] Support")
                    self.stdout.write(f"   [3] Management")

                    while True:
                        get_role = {1: "Sales", 2: "Support", 3: "Management"}
                        try:
                            role_number = int(
                                input("  Please enter your choice for the role: ")
                            )
                            if role_number in get_role:
                                updates["role"] = get_role[role_number]
                                break
                            else:
                                self.stdout.write(
                                    "Invalid role number. "
                                    "Please enter a number between 1 and 3. \n\n"
                                )
                        except ValueError:
                            self.stdout.write(
                                "  Invalid input. Please enter a number. \n\n"
                            )

                if updates:
                    Employee.objects.filter(user=employee.user).update(**updates)
                    self.stdout.write()
                    self.stdout.write("  Here are all information about this employee:")
                    self.stdout.write(f"   Email: {employee.user.email}")
                    self.stdout.write(f"   First name: {employee.first_name}")
                    self.stdout.write(f"   Last name: {employee.last_name}")
                    self.stdout.write(f"   Role: {employee.role} \n\n")

                    self.stdout.write("  The employee was updated. \n\n")
                    break
                else:
                    self.stdout.write("  No changes made. \n\n")
                    break
