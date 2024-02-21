from faker import Faker
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import Employee
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
            for key, value in data.items():
                user = UserModel.objects.create_user(
                    email=value["email"],
                    password="Test",
                )
                if user:
                    Employee.objects.create(
                        user=user,
                        first_name=value["first_name"],
                        last_name=value["last_name"],
                        role=value["role"],
                    )
        except IntegrityError:
            self.stdout.write(self.style.WARNING("   Exists already!"))
        else:
            self.stdout.write(data[1]["email"])
            self.stdout.write(
                self.style.SUCCESS("   Users and Employees successfully created!")
            )
