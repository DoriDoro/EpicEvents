from unittest import TestCase

from django.contrib.auth import get_user_model

from accounts.models import Employee, Client
from contracts.models import Contract

UserModel = get_user_model()


class ContractTestCase(TestCase):
    COSTS = 51236.20
    AMOUNT = 520.60
    SIGNED = "S"
    DRAFT = "D"

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
            state=self.DRAFT,
        )

    def tearDown(self):
        self.user.delete()
        self.employee.delete()
        self.client.delete()
        self.contract.delete()

    def test_contract_creation_successful(self):
        self.assertEqual(self.contract.client, self.client)
        self.assertEqual(self.contract.employee, self.employee)
        self.assertEqual(self.contract.total_costs, self.COSTS)

    def test_contract_creation_failed(self):
        pass

    def test_contract_total(self):
        self.assertEquals(self.contract.total, f"{self.COSTS} €")

    def test_contract_paid_amount(self):
        self.assertEquals(self.contract.paid_amount, f"{self.AMOUNT} €")

    def test_contract_rest_amount(self):
        result = self.COSTS - self.AMOUNT
        self.assertEquals(self.contract.rest_amount, f"{result} €")

    def test_contract_str(self):
        self.assertEquals(
            f"{self.client.get_full_name} ({self.employee.user.email})",
            "John Client (testemployee@mail.com)",
        )
