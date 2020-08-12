from django.core.management.base import BaseCommand, CommandError
from accounti.management.commands._daily_checks import *

class Command(BaseCommand):
    help = 'Daily checks to be performed at every midnight'

    def handle(self, *args, **options):

        check_bundles()
