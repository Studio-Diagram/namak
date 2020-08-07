from django.core.management.base import BaseCommand, CommandError
from accounti.models import *

class Command(BaseCommand):
    help = 'Daily checks to be performed at every midnight'

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            print(user)

            self.stdout.write(self.style.SUCCESS(user))