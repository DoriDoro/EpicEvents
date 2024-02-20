from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import Employee

UserModel = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "This command creates 12 employees as basic data."

    def handle(self, *args, **options):
        data_employee = {}

        # create 12 employee data:
        for i in range(1, 13):
            employee = {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name().upper(),
            }
            data_employee[i] = employee

        try:
            roles = ["SA", "SU", "MA"]

            for role in roles:
                for _ in range(4):
                    for key, data in list(
                        data_employee.items()
                    ):  # Use list() to avoid mutation during iteration
                        user = UserModel.objects.create_user(data["email"], "Test")
                        Employee.objects.create(
                            user=user,
                            first_name=data["first_name"],
                            last_name=data["last_name"],
                            role=role,
                        )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("Exists already!"))
        else:
            self.stdout.write(
                self.style.SUCCESS("Users and Employees successfully created!")
            )
