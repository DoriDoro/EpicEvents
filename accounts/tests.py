from django.test import TestCase

from django.contrib.auth import get_user_model

from accounts.models import Employee, Client

UserModel = get_user_model()


class ModelTestCase(TestCase):
    USER_EMAIL = "testuser@mail.com"
    USER_PASSWORD = "TestPassw0rd!"

    EMPLOYEE_FIRST_NAME = "John"
    EMPLOYEE_LAST_NAME = "Employee"

    CLIENT_FIRST_NAME = "John"
    CLIENT_LAST_NAME = "Client"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            email=cls.USER_EMAIL, password=cls.USER_PASSWORD
        )
        cls.employee = Employee.objects.create(
            user=cls.user,
            first_name=cls.EMPLOYEE_FIRST_NAME,
            last_name=cls.EMPLOYEE_LAST_NAME,
            role="SA",
        )
        cls.custom_client = Client.objects.create(
            employee=cls.employee,
            email="testclient@mail.com",
            first_name=cls.CLIENT_FIRST_NAME,
            last_name=cls.CLIENT_LAST_NAME,
            phone=1234567,
            company_name="Test Company",
        )


class UserModelTestCase(ModelTestCase):
    def test_user_creation_successful(self):
        self.assertEqual(self.user.email, self.USER_EMAIL)
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))

    def test_user_creation_failed(self):
        pass


class EmployeeTestCase(ModelTestCase):
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


class ClientTestCase(ModelTestCase):
    def test_client_creation_successful(self):
        self.assertEqual(self.custom_client.first_name, self.CLIENT_FIRST_NAME)
        self.assertEqual(self.custom_client.last_name, self.CLIENT_LAST_NAME)
        self.assertEqual(self.custom_client.employee.user.email, self.USER_EMAIL)

    def test_client_creation_failed(self):
        pass

    def test_client_full_name(self):
        self.assertEqual(
            self.custom_client.get_full_name,
            f"{self.CLIENT_FIRST_NAME} {self.CLIENT_LAST_NAME}",
        )

    def test_client_str(self):
        self.assertEquals(
            f"{self.custom_client.get_full_name} ({self.employee.get_full_name})",
            f"{self.CLIENT_FIRST_NAME} {self.CLIENT_LAST_NAME} "
            f"({self.EMPLOYEE_FIRST_NAME} {self.EMPLOYEE_LAST_NAME})",
        )
