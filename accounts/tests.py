from unittest import TestCase

from django.contrib.auth import get_user_model

from accounts.models import Employee, Client

UserModel = get_user_model()


class UserModelTestCase(TestCase):
    USER_EMAIL = "testuser@mail.com"
    USER_PASSWORD = "TestPassw0rd!"

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email=self.USER_EMAIL, password=self.USER_PASSWORD
        )

    # to make sure the created user is deleted after the test:
    def tearDown(self):
        self.user.delete()

    def test_user_creation_successful(self):
        self.assertEqual(self.user.email, self.USER_EMAIL)
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))

    def test_user_creation_failed(self):
        pass


class EmployeeTestCase(TestCase):
    USER_EMAIL = "testemployee@mail.com"

    EMPLOYEE_FIRST_NAME = "John"
    EMPLOYEE_LAST_NAME = "Employee"

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email=self.USER_EMAIL, password="TestPassw0rd!"
        )
        self.employee = Employee.objects.create(
            user=self.user,
            first_name=self.EMPLOYEE_FIRST_NAME,
            last_name=self.EMPLOYEE_LAST_NAME,
            role="SA",
        )

    def tearDown(self):
        self.user.delete()
        self.employee.delete()

    def test_employee_creation_successful(self):
        self.assertEqual(self.employee.first_name, self.EMPLOYEE_FIRST_NAME)
        self.assertEqual(self.employee.last_name, self.EMPLOYEE_LAST_NAME)
        self.assertEqual(self.employee.user.email, self.USER_EMAIL)

    def test_employee_creation_failed(self):
        pass

    def test_employee_full_name(self):
        self.assertEquals(
            self.employee.get_full_name,
            f"{self.EMPLOYEE_FIRST_NAME} {self.EMPLOYEE_LAST_NAME}",
        )

    def test_employee_email_address(self):
        self.assertEquals(self.employee.get_email_address, self.USER_EMAIL)

    def test_employee_str(self):
        self.assertEquals(
            f"{self.employee.get_full_name} ({self.employee.role})",
            f"{self.EMPLOYEE_FIRST_NAME} {self.EMPLOYEE_LAST_NAME} (SA)",
        )


class ClientTestCase(TestCase):
    USER_EMAIL = "testemployee@mail.com"

    EMPLOYEE_FIRST_NAME = "John"
    EMPLOYEE_LAST_NAME = "Employee"

    CLIENT_FIRST_NAME = "John"
    CLIENT_LAST_NAME = "Client"

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email=self.USER_EMAIL, password="TestPassw0rd!"
        )
        self.employee = Employee.objects.create(
            user=self.user,
            first_name=self.EMPLOYEE_FIRST_NAME,
            last_name=self.CLIENT_LAST_NAME,
            role="SA",
        )
        self.client = Client.objects.create(
            employee=self.employee,
            email="testclient@mail.com",
            first_name=self.CLIENT_FIRST_NAME,
            last_name=self.CLIENT_LAST_NAME,
            phone=1234567,
            company_name="Test Company",
        )

    def tearDown(self):
        self.user.delete()
        self.employee.delete()
        self.client.delete()

    def test_client_creation_successful(self):
        self.assertEqual(self.client.first_name, self.CLIENT_FIRST_NAME)
        self.assertEqual(self.client.last_name, self.CLIENT_LAST_NAME)
        self.assertEqual(self.client.employee.user.email, self.USER_EMAIL)

    def test_client_creation_failed(self):
        pass

    def test_client_full_name(self):
        self.assertEqual(
            self.client.get_full_name,
            f"{self.CLIENT_FIRST_NAME} {self.CLIENT_LAST_NAME}",
        )

    def test_client_str(self):
        self.assertEquals(
            f"{self.client.get_full_name} ({self.employee.get_full_name})",
            f"{self.CLIENT_FIRST_NAME} {self.CLIENT_LAST_NAME} "
            f"({self.EMPLOYEE_FIRST_NAME} {self.EMPLOYEE_LAST_NAME})",
        )
