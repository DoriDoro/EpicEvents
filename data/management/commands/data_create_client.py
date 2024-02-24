from faker import Faker
from django.db import IntegrityError

from accounts.models import Client, Employee
from cli.utils_messages import create_success_message, create_error_message
from data.utils_data_custom_command import DataCreateCommand

fake = Faker()


class Command(DataCreateCommand):
    """
    Command for creating basic data for 40 clients. This command is part of a larger system for
    generating and populating the database with basic client data. It is designed to create
    40 clients with various attributes such as name, email, phone, and company name.
    The clients are associated with employees who have the role of "SA" (Sales). If a client with
    the same email already exists, an IntegrityError is caught and handled appropriately.

    Attributes:
        help (str): Description of the command.

    Methods:
        get_queryset(self): Initializes the queryset for employees with the role of "SA".
        create_fake_data(self): Generates fake data for 40 clients and returns a dictionary
            with the data.
        create_instances(self, data): Creates instances of Client model in the database
            using the provided data.

    Raises:
        IntegrityError: If there is an attempt to create a client with an email that
            already exists in the database.
    """

    help = "This command creates 40 clients as basic data."

    def get_queryset(self):
        self.employee = Employee.objects.filter(role="SA")

    def create_fake_data(self):
        data_client = {}

        for i in range(1, 41):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@mail.com"

            employee = self.employee[(i - 1) % len(self.employee)]

            client = {
                "employee": employee,
                "email": email,
                "first_name": first_name,
                "last_name": last_name.upper(),
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
            create_error_message("There are clients which")
        else:
            create_success_message("Clients", "created")
