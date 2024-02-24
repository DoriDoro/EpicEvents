from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    """
    This model represents an event with various attributes such as contract, employee, date, name,
    location, max_guests, and notes.

    - `contract` (ForeignKey): A foreign key to the Contract model, representing the contract
        associated with the event.
    - `employee` (ForeignKey): A foreign key to the Employee model, representing the employee
        assigned to the event.
    - `date` (DateTimeField): The date and time when the event is scheduled to take place.
    - `name` (CharField): The name of the event.
    - `location` (CharField): The address where the event will take place.
    - `max_guests` (PositiveIntegerField): The maximum number of guests allowed for the event.
    - `notes` (TextField): Additional notes or details about the event.

    The `__str__` method returns a string representation of the event, including its name and
    the email of the associated employee.
    """

    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.CASCADE,
        related_name="event_contracts",
        verbose_name=_("contract for event"),
    )
    employee = models.ForeignKey(
        "accounts.Employee",
        on_delete=models.CASCADE,
        related_name="event_employees",
        verbose_name=_("employee for event"),
    )
    date = models.DateTimeField(default=timezone.now, verbose_name=_("date of event"))
    name = models.CharField(max_length=100, verbose_name=_("name of event"))
    location = models.CharField(max_length=200, verbose_name=_("address of event"))
    max_guests = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1,
                _(
                    "Impossible to create an event with the number of guests less than 1 guest."
                ),
            )
        ],
        verbose_name=_("number of guests"),
    )
    notes = models.TextField(verbose_name=_("notes for the event"))

    def __str__(self):
        return f"{self.name} ({self.employee.user.email})"
