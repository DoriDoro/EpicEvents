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
        roles = ["SA", "SU", "MA"]
        data_employee = {}

        for i in range(1, 13):
            # Use modulo operation to cycle through the roles
            role = roles[(i - 1) % len(roles)]
            employee = {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name().upper(),
                "role": role,
            }
            data_employee[i] = employee

        try:
            for key, data in list(data_employee.items()):
                user, created = UserModel.objects.get_or_create(
                    email=data["email"],
                    defaults={"email": data["email"], "password": "Test"},
                )
                if created:
                    Employee.objects.create(
                        user=user,
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        role=data["role"],
                    )
        except IntegrityError:
            self.stdout.write(self.style.WARNING("   Exists already!"))
        else:
            self.stdout.write(
                self.style.SUCCESS("   Users and Employees successfully created!")
            )
