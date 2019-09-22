from django.db import models

# Create your models here.
class Tienda(models.Model):
    nombre = models.CharField(
        max_length=150
    )
    slug = models.SlugField(
        blank=True,
        null=True,
        max_length=150
    )

    def __str__(self):
        return u"{} id, nombre {}.".format(self.id, 
                        self.nombre)


class Dias(models.Model):
    '''
    DIAS DE LA SEMANA
        (0, 'Lunes'),
        (1, 'Martes'),
        ...
        (6, 'Domingo'),
    )
    '''
    valor = models.SmallIntegerField(
        default=0
    ) #usado para ordenar los dias
    dia = models.CharField(
        max_length=12
    )
    def __str__(self):
        return "{} {}".format(self.valor, self.dia)


class TiendaWorkingWindow(models.Model):
    dias = models.ManyToManyField( #weekday
        Dias, blank=True
    )
    tienda = models.ForeignKey(
        Tienda,
        db_index=True,
        on_delete=models.PROTECT
    )
    start_time = models.TimeField() #opens
    end_time = models.TimeField()   #closes
