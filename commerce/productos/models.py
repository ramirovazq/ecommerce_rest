from django.db import models
from tienda.models import Tienda

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(
        max_length=150
    )
    slug = models.SlugField(
        blank=True,
        null=True,
        max_length=150
    )
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.PROTECT,
        verbose_name='Tiendas',
    )
    precio = models.DecimalField(
    	max_digits=8, 
    	decimal_places=3, 
    	default=0.0
    )
    tiempo_de_elaboracion = models.PositiveIntegerField(
    	default=0,
    	blank=True,
    )

    def __str__(self):
        return u"{} id, nombre {}, tienda {}.".format(self.id, 
                        self.nombre, self.tienda)
