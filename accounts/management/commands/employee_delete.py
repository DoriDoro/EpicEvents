from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import Employee


class Command(BaseCommand):
    help = "Delete an employee."

    def handle(self, *args, **options):
        while True:
            email = input(" Please enter the email address to delete the employee: ")
            employee = Employee.objects.filter(user__email=email).first()
            if employee is None:
                self.stdout.write(
                    "   This email address is not known. Please enter a valid email address. \n\n"
                )
            else:
                try:
                    delete_employee = input(
                        f"  Do you want to delete this employee {employee.user.email}? (yes/no): "
                    ).lower()

                    if delete_employee in ["yes", "y"]:
                        employee.delete()
                        self.stdout.write(f" The employee {email} was deleted!")
                        break
                    if delete_employee in ["no", "n"]:
                        possible_exit = input(
                            "   Do you want to delete an other employee (yes) "
                            "or do you want to go back to the main menu? (*): "
                        )
                        if possible_exit == "*":
                            call_command("start")
                            break
                except ValueError:
                    self.stdout.write("Invalid input.")
