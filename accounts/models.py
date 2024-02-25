from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    The `UserManager` class is a custom manager for the `User` model, extending Django's
    `BaseUserManager`. It provides methods for creating users and superusers, ensuring that email
    addresses are normalized and that superusers have the appropriate permissions set.

    - `create_user`: Creates a new user with the given email and password. It normalizes the email
        address and sets the password. This method is designed to handle the creation
        of regular users.
    - `create_superuser`: Creates a new superuser with the given email and password. It ensures
        that superusers have `is_staff`, `is_superuser`, and `is_active` set to `True`.
        This method is specifically for creating superusers with full permissions.

    These methods are essential for managing user accounts within a Django application, providing
    a secure and flexible way to handle user authentication and authorization. By using custom
    methods for creating users and superusers, the `UserManager` allows for the implementation of
    custom logic and validation that aligns with the specific requirements of the application.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    This class `User` is a custom user model for Django applications, designed to use email
    addresses as the primary identifier for user authentication instead of traditional usernames.
    It extends `AbstractUser` to inherit all the fields and methods necessary for user management,
    including authentication and authorization.

    - `username`: This field is set to `None` to indicate that email addresses will be used for
        authentication instead of usernames.
    - `email` (EmailField): An `EmailField` that is marked as unique, ensuring that each email address can only
        be associated with one user account.

    - `USERNAME_FIELD`: Specifies the field to be used as the unique identifier for authentication,
        which is set to `'email'`.
    - `REQUIRED_FIELDS`: Specifies additional fields that must be filled out when creating a user.
        Since the email field is required and unique, this list is empty.

    - `objects`: Assigns the custom `UserManager` to handle the creation of user and superuser
        instances.

    The `UserManager` class, `UserManager`, is a custom manager for the `User` model. It provides
    methods for creating users and superusers, ensuring that email addresses are normalized and
    that superusers have the appropriate permissions set.

    - `create_user`: Creates a new user with the given email and password. It normalizes the email
        address and sets the password.
    - `create_superuser`: Creates a new superuser with the given email and password. It ensures
        that superusers have `is_staff`, `is_superuser`, and `is_active` set to `True`.

    This custom user model allows for a more straightforward authentication flow, where users log
    in using their email addresses, and it provides a flexible foundation for customizing user
    management features in Django applications.
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Employee(models.Model):
    """
    The `Employee` model represents employees within the system, with different roles such as
    Sales, Support, and Management. Each employee is associated with a user account, allowing for
    authentication and authorization based on their role.

    - `ROLE_CHOICES`: A dictionary defining the possible roles an employee can have, including
        Sales, Support, and Management.

    - `user` (ForeignKey): A one-to-one relationship with the `User` model, establishing a link between an
        employee and their user account. This field is crucial for authentication
        and authorization purposes.
    - `first_name` and `last_name` (CharField): Char fields for storing the employee's first and last names.
    - `role` (CharField): A char field with choices defined by `ROLE_CHOICES`, specifying the employee's role
        within the organization.

    Property methods include:
    - `get_full_name`: A property method that returns the employee's full name, combining
        the first and last names.
    - `get_email_address`: A property method that retrieves the associated user's email address.

    The `__str__` method returns a string representation of the employee, displaying
        their full name and role.
    """

    SALES = "SA"
    SUPPORT = "SU"
    MANAGEMENT = "MA"

    ROLE_CHOICES = {
        SALES: _("Sales"),
        SUPPORT: _("Support"),
        MANAGEMENT: _("Management"),
    }

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="employee_users",
        verbose_name=_("employee"),
    )
    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"))
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, verbose_name=_("role"))

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_email_address(self):
        return self.user.email

    def __str__(self):
        return f"{self.get_full_name} ({self.role})"


class Client(models.Model):
    """
    The `Client` model represents clients associated with employees within the system.
    Each client is linked to an employee, indicating who is responsible for their account.

    - `employee` (ForeignKey): A foreign key relationship to the `Employee` model, linking each
        client to their assigned employee.
    - `email` (ForeignKey): An email field that stores the client's email address, ensuring
        uniqueness to prevent duplicate client entries.
    - `first_name`, `last_name`, `phone`, and `company_name` (CharField): Char fields for storing
        the client's personal information and company name.
    - `created_on` and `last_update`: DateTime fields that automatically record the creation
        and last update times of a client record.

    Property methods include:
    - `get_full_name`: A property method that returns the client's full name, combining
        the first and last names.
    - `get_email_address`: A property method that retrieves the associated employee's
        user's email address.

    The `__str__` method returns a string representation of the client, displaying their full name.

    These models are essential for managing employees and clients within a Django application,
    providing a structured way to store and access user and client information. The relationships
    between the models ensure that each client is associated with an employee,
    facilitating role-based access control and data management.
    """

    employee = models.ForeignKey(
        "accounts.Employee",
        on_delete=models.CASCADE,
        related_name="client_employee",
        verbose_name=_("employee"),
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name=_("email address")
    )
    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"))
    phone = models.CharField(max_length=17, verbose_name=_("phone number"))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_("last updated on"))
    company_name = models.CharField(max_length=200, verbose_name=_("company name"))

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.get_full_name} ({self.employee.get_full_name})"
