from datetime import datetime

from django.db import IntegrityError
from django.utils.timezone import make_aware
from faker import Faker

from cli.utils_messages import create_success_message, create_error_message
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

        for i in range(1, 11):
            date_object = fake.date_time()
            date_object = make_aware(date_object)

            event_term = fake.word(
                ext_word_list=["conference", "workshop", "meetup", "gathering"]
            )

            contract = self.contract[(i - 1) % len(self.contract)]

            event = {
                "contract": contract,
                "employee": contract.employee,
                "date": date_object,
                "name": f"{fake.name()} {event_term}",
                "location": fake.address(),
                "max_guests": fake.random_int(min=50, max=1000),
                "notes": fake.text(),
            }
            data_event[i] = event

        return data_event

    def create_instances(self, data):
        try:
            for d in data.values():
                Event.objects.create(**d)

        except IntegrityError:
            create_error_message("There are events which")
        else:
            create_success_message("Events", "created")
