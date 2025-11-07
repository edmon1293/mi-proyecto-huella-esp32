from django.core.management.base import BaseCommand
from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuserCommand

class Command(CreateSuperuserCommand):
    def handle(self, *args, **options):
        # Modifica el manejo para no exigir ciertos campos para superusuarios
        options['skip_validation'] = True
        super().handle(*args, **options)