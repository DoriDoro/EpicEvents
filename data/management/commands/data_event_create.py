from datetime import datetime

from django.db import IntegrityError
from django.utils.timezone import make_aware
from faker import Faker

from contracts.models import Contract
from data.utils_data_custom_command import DataCreateCommand
from events.models import Event

fake = Faker()


class Command(DataCreateCommand):
    help = "Creates 50 events."

    def get_queryset(self):
        self.contract = Contract.objects.select_related("employee").all()

    def create_fake_data(self):
        data_event = {}

        for i in range(1, 51):
            date_object = fake.date()
            date_object = datetime.strptime(date_object, "%Y-%m-%d")
            date_object = make_aware(date_object)

            event = {
                "date": date_object,
                "name": fake.name(),
                "location": fake.address(),
                "max_guests": fake.random_int(min=50, max=1000),
                "notes": fake.text(),
            }
            data_event[i] = event

        return data_event

    def create_instances(self, data):
        try:
            for contract in self.contract:
                for d in data.values():
                    Event.objects.create(
                        contract=contract, employee=contract.employee, **d
                    )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("Exists already!"))
        else:
            self.stdout.write(self.style.SUCCESS("Events successfully created!"))
