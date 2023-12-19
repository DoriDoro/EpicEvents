from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.CASCADE,
        related_name="event_contracts",
        verbose_name=_("contract for event"),
    )
    account_manager = models.ForeignKey(
        "accounts.AccountManager",
        on_delete=models.CASCADE,
        related_name="event_account_managers",
        verbose_name=_("account manager for event"),
    )
    event_date = models.DateTimeField(
        default=timezone.now(), verbose_name=_("date of event")
    )
    event_name = models.CharField(max_length=100, verbose_name=_("name of event"))
    event_location = models.CharField(
        max_length=200, verbose_name=_("address of event")
    )
    max_number_guests = models.PositiveIntegerField(
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
    event_notes = models.TextField(verbose_name=_("notes for the event"))
