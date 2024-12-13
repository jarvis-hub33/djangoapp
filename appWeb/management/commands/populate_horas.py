from django.core.management.base import BaseCommand
from appWeb.models import HoraDisponible
from datetime import time

class Command(BaseCommand):
    help = 'Poblar horas disponibles para las especialidades'

    def handle(self, *args, **kwargs):
        horas = [
            time(hour=8, minute=0),
            time(hour=8, minute=40),
            time(hour=9, minute=20),
            time(hour=10, minute=0),
            time(hour=10, minute=40),
            time(hour=11, minute=20),
            time(hour=12, minute=0),
            time(hour=12, minute=40),
            time(hour=13, minute=20),
            time(hour=14, minute=0),
        ]

        especialidades = ['odontologia', 'medicina_general', 'retiro_insumos']

        for especialidad in especialidades:
            for hora in horas:
                HoraDisponible.objects.get_or_create(especialidad=especialidad, hora=hora)

        self.stdout.write(self.style.SUCCESS("Horas disponibles pobladas correctamente."))
