from unittest import TestCase

from django.contrib.auth import get_user_model

from accounts.models import Employee, Client

UserModel = get_user_model()


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email="testuser@mail.com", password="TestPassw0rd!"
        )

    # to make sure the created user is deleted after the test:
    def tearDown(self):
        self.user.delete()

    def test_user_creation_successful(self):
        self.assertEqual(self.user.email, "testuser@mail.com")
        self.assertTrue(self.user.check_password("TestPassw0rd!"))

    def test_user_creation_failed(self):
        pass


class EmployeeTestCase(TestCase):
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

    def tearDown(self):
        self.user.delete()
        self.employee.delete()

    def test_employee_creation_successful(self):
        self.assertEqual(self.employee.first_name, "John")
        self.assertEqual(self.employee.last_name, "Employee")
        self.assertEqual(self.employee.user.email, "testemployee@mail.com")

    def test_employee_creation_failed(self):
        pass

    def test_employee_full_name(self):
        self.assertEquals(self.employee.get_full_name, "John Employee")

    def test_employee_email_address(self):
        self.assertEquals(self.employee.get_email_address, "testemployee@mail.com")

    def test_employee_str(self):
        self.assertEquals(
            f"{self.employee.get_full_name} ({self.employee.role})",
            "John Employee (SA)",
        )


class ClientTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email="testemployee@mail.com", password="TestPassw0rd!"
        )
        self.employee = Employee.objects.create(
            user=self.user, first_name="Test", last_name="Employee", role="SA"
        )
        self.client = Client.objects.create(
            employee=self.employee,
            email="testclient@mail.com",
            first_name="John",
            last_name="Client",
            phone=1234567,
            company_name="Test Company",
        )

    def tearDown(self):
        self.user.delete()
        self.employee.delete()
        self.client.delete()

    def test_client_creation_successful(self):
        self.assertEqual(self.client.first_name, "John")
        self.assertEqual(self.client.last_name, "Client")
        self.assertEqual(self.client.employee.user.email, "testemployee@mail.com")

    def test_client_creation_failed(self):
        pass

    def test_client_full_name(self):
        self.assertEqual(self.client.get_full_name, "John Client")

    def test_client_str(self):
        self.assertEquals(
            f"{self.client.get_full_name} ({self.employee.get_full_name})",
            "John Client (Test Employee)",
        )
