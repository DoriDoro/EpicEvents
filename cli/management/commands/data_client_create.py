from faker import Faker
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Client, Employee

fake = Faker()


class Command(BaseCommand):
    help = "This command creates 20 clients as basic data."

    def handle(self, *args, **options):
        data_client = {}

        for i in range(1, 21):
            client = {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "phone": fake.bothify("########"),
                "company_name": fake.company(),
            }
            data_client[i] = client

        employees = Employee.objects.filter(role="SA")

        try:
            for employee in employees:
                for data in data_client.values():
                    Client.objects.create(employee=employee, **data)

        except IntegrityError:
            self.stdout.write(self.style.WARNING("Exists already!"))
        else:
            self.stdout.write(
                self.style.SUCCESS("Users and Employees successfully created!")
            )
