from django.db import models
from tienda.models import Tienda
from productos.models import Producto

# Create your models here.
class Orden(models.Model):
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.PROTECT,
    )
    fecha_de_entrega_usuario = models.DateField(        
    )
    precio_total_orden = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True
    )


class Item(models.Model):
    orden = models.ForeignKey(
        Orden,
        on_delete=models.PROTECT
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(
    	default=1,
    	blank=True,
    )
    precio_unitario = models.DecimalField(
    	max_digits=8, 
    	decimal_places=2, 
    	default=0.0
    )
    precio_total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.0
    )
