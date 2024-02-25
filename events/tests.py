from unittest import TestCase

from django.contrib.auth import get_user_model

from accounts.models import Employee, Client
from contracts.models import Contract
from events.models import Event

UserModel = get_user_model()


class EventTestCase(TestCase):
    COSTS = 51236.20
    AMOUNT = 520.60
    SIGNED = "S"

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email="testemployee@mail.com", password="TestPassw0rd!"
        )
        self.employee = Employee.objects.create(
            user=self.user,
            first_name="John",
            last_name="Employee",
            role="SA",
        )
        self.client = Client.objects.create(
            employee=self.employee,
            email="testclient@mail.com",
            first_name="John",
            last_name="Client",
            phone="1234567890",
            company_name="Test Company",
        )
        self.contract = Contract.objects.create(
            client=self.client,
            employee=self.employee,
            total_costs=self.COSTS,
            amount_paid=self.AMOUNT,
            state=self.SIGNED,
        )
        self.event = Event.objects.create(
            contract=self.contract,
            employee=self.employee,
            name="Test Event",
            location="Test Address",
            max_guests=652,
            notes="Test Text",
        )

    def tearDown(self):
        self.user.delete()
        self.employee.delete()
        self.client.delete()
        self.contract.delete()
        self.event.delete()

    def test_event_creation_successful(self):
        self.assertEqual(self.event.contract.client, self.client)
        self.assertEqual(self.event.employee, self.employee)
        self.assertEqual(self.event.location, "Test Address")

    def test_event_creation_failed(self):
        pass

    def test_event_str(self):
        self.assertEquals(
            f"{self.event.name} ({self.employee.user.email})",
            "Test Event (testemployee@mail.com)",
        )
