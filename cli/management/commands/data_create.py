from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import Employee

UserModel = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "This command creates 12 employees and 30 clients as basic data."

    def handle(self, *args, **options):
        data_employee = {}
        data_client = {}

        # create 12 employee data:
        for i in range(1, 13):
            employee = {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name().upper(),
            }
            data_employee[i] = employee

        # create 30 client data:
        for i in range(1, 31):
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name().upper()
            phone = fake.bothify("########")
            company_name = fake.company()
            data_client[i] = {email, first_name, last_name, phone, company_name}

        try:
            for i in range(4):
                for key, data in data_employee.items():
                    data_employee.pop(key, None)
                    user = UserModel.objects.create_user(data["email"], "Test")
                    Employee.objects.create(
                        user=user,
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        role="SA",
                    )
            for i in range(4):
                for key, data in data_employee.items():
                    data_employee.pop(key, None)
                    user = UserModel.objects.create_user(data["email"], "Test")
                    Employee.objects.create(
                        user=user,
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        role="SU",
                    )
            for i in range(4):
                for key, data in data_employee.items():
                    data_employee.pop(key, None)
                    user = UserModel.objects.create_user(data["email"], "Test")
                    Employee.objects.create(
                        user=user,
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        role="MA",
                    )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("Exists already!"))
        else:
            self.stdout.write(self.style.SUCCESS("User successfully created!"))
