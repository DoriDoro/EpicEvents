from faker import Faker
from django.db import IntegrityError

from accounts.models import Client, Employee
from data.utils_data_custom_command import DataCreateCommand

fake = Faker()


class Command(DataCreateCommand):
    help = "This command creates 20 clients as basic data."

    def get_queryset(self):
        self.employee = Employee.objects.filter(role="SA")

    def create_fake_data(self):
        data_client = {}

        for i in range(1, 21):
            employee = self.employee[(i - 1) % len(self.employee)]

            client = {
                "employee": employee,
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "phone": fake.bothify("########"),
                "company_name": fake.company(),
            }
            data_client[i] = client

        return data_client

    def create_instances(self, data):
        try:
            for d in data.values():
                Client.objects.create(**d)

        except IntegrityError:
            self.stdout.write(self.style.WARNING("Exists already!"))
        else:
            self.stdout.write(
                self.style.SUCCESS("Users and Employees successfully created!")
            )
