# Generated by Django 5.0 on 2024-01-12 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total_costs",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        verbose_name="total costs of contract",
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="contract created on"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[("S", "Signed"), ("D", "Draft")],
                        default="D",
                        max_length=1,
                        verbose_name="state",
                    ),
                ),
                (
                    "account_manager",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contract_account_managers",
                        to="accounts.accountmanager",
                        verbose_name="account manager of contract",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contract_clients",
                        to="accounts.client",
                        verbose_name="client of contract",
                    ),
                ),
            ],
        ),
    ]