from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
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
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Employee(models.Model):
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

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # def get_email_address(self):
    #     return self.user.email

    def __str__(self):
        return self.get_full_name()


class Client(models.Model):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name=_("email address")
    )
    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"))
    phone = models.CharField(max_length=17, verbose_name=_("phone number"))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_("last updated on"))
    company_name = models.CharField(max_length=200, verbose_name=_("company name"))

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # def get_email_address(self):
    #     return self.user.email

    def __str__(self):
        return self.get_full_name()
