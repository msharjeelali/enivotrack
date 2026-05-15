from django.core.management.base import BaseCommand
from faker import Faker

from shared.models import Owner, Vehicle

emails = [
    "l226721@lhr.nu.edu.pk",
    "l226744@lhr.nu.edu.pk",
    "l226693@lhr.nu.edu.pk",
    "l226595@lhr.nu.edu.pk",
    "l226733@lhr.nu.edu.pk",
    "l226826@lhr.nu.edu.pk",
    "l226916@lhr.nu.edu.pk",
]


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):

        fake = Faker()

        for _ in range(7):
            owner = Owner.objects.create(
                name=fake.name(),
                email=emails[_ % len(emails)],
            )
            self.stdout.write(self.style.SUCCESS(f'Created owner: {owner.name}'))

        for _ in range(30):
            vehicle = Vehicle.objects.create(
                plate=fake.license_plate(),
                make=fake.company(),
                model=fake.word(),
                year=fake.year(),
                capacity = fake.random_int(min=660, max=4000),
                body_type=fake.random_element(elements=[choice[0] for choice in Vehicle.BODY_TYPE_CHOICES]),
                owner=Owner.objects.order_by('?').first()
            )
            self.stdout.write(self.style.SUCCESS(f'Created vehicle: {vehicle.make} {vehicle.model}'))
