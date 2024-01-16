from django.core.management.base import BaseCommand

from accounts.models import Client


class Command(BaseCommand):
    help = "Prompts for details to update a client."

    def handle(self, *args, **options):
        while True:
            email = input(" Please enter the email address to update the client: ")
            client = Client.objects.filter(user__email=email).first()
            if client is None:
                self.stdout.write(
                    "   This email address is not known. Please enter a valid email address. \n\n"
                )
            else:
                self.stdout.write("   Here are all information about this client:")
                self.stdout.write(f"    Email: {email}")
                self.stdout.write(f"    First name: {client.first_name}")
                self.stdout.write(f"    Last name: {client.last_name}")
                self.stdout.write(f"    Phone: {client.phone}")
                self.stdout.write(f"    Company name: {client.company_name} \n\n")

                updates = {}
                update_f_name = input(
                    " Do you want to update the first name? (yes/no): "
                ).lower()
                if update_f_name in ["yes", "y"]:
                    f_name = input("  Please enter the new first name: ")
                    updates["first_name"] = f_name

                update_l_name = input(
                    " Do you want to update the last name? (yes/no): "
                ).lower()
                if update_l_name in ["yes", "y"]:
                    l_name = input("  Please enter the new last name: ")
                    updates["last_name"] = l_name

                update_phone = input(
                    " Do you want to update the phone? (yes/no): "
                ).lower()
                if update_phone in ["yes", "y"]:
                    phone = input("  Please enter the new phone number: ")
                    updates["phone"] = phone

                update_company_name = input(
                    " Do you want to update the company name? (yes/no): "
                ).lower()
                if update_company_name in ["yes", "y"]:
                    company_name = input("  Please enter the new company name: ")
                    updates["company_name"] = company_name

                if updates:
                    Client.objects.filter(user__email=email).update(**updates)
                    self.stdout.write("  The client was updated. \n\n")
                    break
                else:
                    self.stdout.write("  No changes made. \n\n")
                    break
