from django.db import models
from django.utils.translation import gettext_lazy as _


class Contract(models.Model):
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

    # TODO: add amount_paid as attribute and amount_remaining as property
