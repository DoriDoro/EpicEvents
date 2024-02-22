from django.contrib.auth.hashers import make_password
from faker import Faker
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import Employee
from cli.utils_messages import create_error_message, create_success_message
from data.utils_data_custom_command import DataCreateCommand

UserModel = get_user_model()
fake = Faker()


class Command(DataCreateCommand):
    help = "This command creates 12 employees as basic data."

    def get_queryset(self):
        pass

    def create_fake_data(self):
        roles_choices = ["SA", "SU", "MA"]
        data_employee = {}

        for i in range(1, 13):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@mail.com"

            # Use modulo operation to cycle through the roles
            role = roles_choices[(i - 1) % len(roles_choices)]
            employee = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name.upper(),
                "role": role,
            }
            data_employee[i] = employee

        return data_employee

    def create_instances(self, data):
        try:
            users_to_create = []
            employees_to_create = []

            for value in data.values():
                user = UserModel(email=value["email"], password=make_password("Test"))
                users_to_create.append(user)

                employee = Employee(
                    user=user,
                    first_name=value["first_name"],
                    last_name=value["last_name"],
                    role=value["role"],
                )
                employees_to_create.append(employee)

            # Bulk create users and employees
            UserModel.objects.bulk_create(users_to_create)
            Employee.objects.bulk_create(employees_to_create)

        except IntegrityError:
            create_error_message("There are employees which")
        else:
            self.stdout.write(data[1]["email"])
            create_success_message("Users and Employees", "created")
