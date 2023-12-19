from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class AccountManager(models.Model):
    SALES = "SA"
    SUPPORT = "SU"
    MANAGEMENT = "MA"

    ROLES = [
        (SALES, _("Sales")),
        (SUPPORT, _("Support")),
        (MANAGEMENT, _("Management")),
    ]

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="account_manager_users",
        verbose_name=_("account manager"),
    )
    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"))
    role = models.CharField(max_length=2, CHOICES=ROLES, verbose_name=_("role"))


class Client(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="client_users",
        verbose_name=_("client"),
    )
    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"))
    # phone
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_("last updated on"))
    company_name = models.CharField(max_length=200, verbose_name=_("company name"))
