from django.db import IntegrityError
from faker import Faker

from accounts.models import Client, Employee
from cli.utils_messages import create_error_message, create_success_message
from contracts.models import Contract
from data.utils_data_custom_command import DataCreateCommand


fake = Faker()


class Command(DataCreateCommand):
    """
    Command to create 30 contracts. This command is designed to generate and create 30 contracts
    with fake data. It selects clients and employees randomly from the database and assigns them
    to contracts with varying states. The command also generates fake total costs and amount paid
    for each contract. If there are any integrity errors during the creation process,
    it handles them appropriately.

    Attributes:
        help (str): Description of the command.

    Methods:
        get_queryset(self): Initializes the queryset for clients, selecting them in a random order.
        create_fake_data(self): Generates fake data for 30 contracts and returns a dictionary
            with the data.
        create_instances(self, data): Creates instances of Contract model in the database using
            the provided data.

    Raises:
        IntegrityError: If there is an attempt to create a contract that violates database
            integrity constraints.
    """

    help = "This command creates 30 contracts."

    def get_queryset(self):
        self.client = Client.objects.select_related("employee").all().order_by("?")

    def create_fake_data(self):
        state_choices = ["S", "S", "S", "D"]
        data_contract = {}

        for i in range(1, 31):
            client = self.client[(i - 1) % len(self.client)]
            state = state_choices[(i - 1) % len(state_choices)]

            contract = {
                "client": client,
                "employee": client.employee,
                "total_costs": fake.pydecimal(
                    left_digits=5, right_digits=2, positive=True
                ),
                "amount_paid": fake.pydecimal(
                    left_digits=3, right_digits=2, positive=True
                ),
                "state": state,
            }
            data_contract[i] = contract

        return data_contract

    def create_instances(self, data):
        try:
            for value in data.values():
                Contract.objects.create(**value)

        except IntegrityError:
            create_error_message("There are contracts which")
        else:
            create_success_message("Contracts", "created")
