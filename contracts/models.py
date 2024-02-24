from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class Contract(models.Model):
    """
    The `Contract` model represents a contract between a client and an employee within a system.
    It is designed to track the financial details of a contract, including the total costs,
    the amount paid, and the state of the contract (either signed or draft).

    - `SIGNED` and `DRAFT`: Constants representing the possible states a contract can be in.
    - `STATE_CHOICES`: A dictionary mapping the state constants to human-readable labels.

    - `client` (ForeignKey): A foreign key to the `Client` model, indicating the client associated
        with the contract.
    - `employee` (ForeignKey): A foreign key to the `Employee` model, indicating the employee
        associated with the contract.
    - `total_costs` (DecimalField): A decimal field representing the total cost of the contract.
    - `amount_paid` (DecimalField): A decimal field representing the amount paid towards the
        contract.
    - `create_date` (DateTimeField): A datetime field automatically set to the current date and
        time when the contract is created.
    - `state` (CharField): A char field with choices defined by `STATE_CHOICES`, indicating the
        current state of the contract.

    Property methods include:
    - `total`: Returns the total costs of the contract formatted as a string
        with a currency symbol.
    - `paid_amount`: Returns the amount paid towards the contract formatted as a string
        with a currency symbol.
    - `rest_amount`: Calculates the remaining amount to be paid on the contract by subtracting
        the amount paid from the total costs, and returns it formatted as a string
        with a currency symbol.

    The `__str__` method returns a string representation of the contract, displaying the full name
    of the client and the email of the associated employee.

    This model is essential for managing contracts within a Django application, providing a
    structured way to store and access contract information. The use of `on_delete=models.CASCADE`
    for both `client` and `employee` foreign keys ensures that when a client or employee
    is deleted, all associated contracts are also deleted to maintain data integrity.
    """

    SIGNED = "S"
    DRAFT = "D"

    STATE_CHOICES = {SIGNED: _("Signed"), DRAFT: _("Draft")}

    client = models.ForeignKey(
        "accounts.Client",
        on_delete=models.CASCADE,
        related_name="contract_clients",
        verbose_name=_("client of contract"),
    )
    employee = models.ForeignKey(
        "accounts.Employee",
        on_delete=models.CASCADE,
        related_name="contract_employees",
        verbose_name=_("Employee of contract"),
    )
    total_costs = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name=_("total costs of contract")
    )
    amount_paid = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name=_("paid amount of contract")
    )
    create_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("contract created on")
    )
    state = models.CharField(
        max_length=1, choices=STATE_CHOICES, default=DRAFT, verbose_name=_("state")
    )

    @property
    def total(self):
        return f"{self.total_costs} €"

    @property
    def paid_amount(self):
        return f"{self.amount_paid} €"

    @property
    def rest_amount(self):
        # Convert the fields to Decimal before performing the calculation
        total_costs_decimal = Decimal(str(self.total_costs))
        amount_paid_decimal = Decimal(str(self.amount_paid))

        rest_amount = total_costs_decimal - amount_paid_decimal

        return f"{rest_amount} €"

    def __str__(self):
        return f"{self.client.get_full_name} ({self.employee.user.email})"
