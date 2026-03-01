from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Setup site for OAuth'

    def handle(self, *args, **options):
        site = Site.objects.get_or_create(
            id=1,
            defaults={'domain': '127.0.0.1:8000', 'name': 'Vishwa E-cart'}
        )
        self.stdout.write(self.style.SUCCESS('Site setup complete!'))
