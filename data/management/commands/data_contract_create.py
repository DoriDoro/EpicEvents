from django.db import IntegrityError
from faker import Faker

from accounts.models import Client, Employee
from contracts.models import Contract
from data.utils_data_custom_command import DataCreateCommand


fake = Faker()


class Command(DataCreateCommand):
    help = "Creates 20 contracts."

    def get_queryset(self):
        self.client = Client.objects.all().order_by("?")
        self.employee = Employee.objects.filter(role="MA").order_by("?")

    def create_fake_data(self):
        state_choices = ["S", "S", "S", "D"]
        data_contract = {}

        for i in range(1, 21):
            client = self.client[(i - 1) % len(self.client)]
            employee = self.employee[(i - 1) % len(self.employee)]
            state = state_choices[(i - 1) % len(state_choices)]

            contract = {
                "client": client,
                "employee": employee,
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
            self.stdout.write(self.style.WARNING("Exists already!"))
        else:
            self.stdout.write(self.style.SUCCESS("Contracts successfully created!"))
