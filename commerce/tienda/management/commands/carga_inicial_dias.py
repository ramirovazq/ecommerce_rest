from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from tienda.models import Dias

class Command(BaseCommand):
    help = 'Carga inicial de tabla de dias de la semana.'
    def handle(self, *args, **options):
        DIAS_DE_LA_SEMANA = (
            (0, 'Lunes'),
            (1, 'Martes'),
            (2, 'Miércoles'),
            (3, 'Jueves'),
            (4, 'Viernes'),
            (5, 'Sábado'),
            (6, 'Domingo'),
        )
        for x in DIAS_DE_LA_SEMANA:            
            obj, bandera = Dias.objects.get_or_create(valor=x[0], dia=x[1])
            if bandera:
                self.stdout.write(self.style.SUCCESS('Dia creado: {} [{}]'.format(obj.valor, obj.dia)))
            else:
                self.stdout.write(self.style.ERROR('Dia ya existia: {} [{}]'.format(obj.valor, obj.dia)))