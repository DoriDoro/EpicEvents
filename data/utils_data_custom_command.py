from django.core.management import BaseCommand


class DataCreateCommand(BaseCommand):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.employee = None
        self.client = None
        self.contract = None
        self.event = None

    def get_queryset(self):
        """
        Requests the queryset of a model.

        Returns:
            queryset: Returns the requested queryset.
        """
        pass

    def create_fake_data(self):
        return dict()

    def create_instances(self, data):
        pass

    def handle(self, *args, **options):
        self.get_queryset()
        fake_data = self.create_fake_data()
        self.create_instances(fake_data)
