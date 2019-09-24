from rest_framework import serializers
from .models import *
from productos.models import Producto
from tienda.models import Tienda

class ItemSpecificSerializer(serializers.Serializer):
    slug = serializers.SlugField(allow_blank=False, max_length=100)
    cantidad = serializers.IntegerField(min_value=1, max_value=100)
    precio_unitario = serializers.DecimalField(min_value=1, max_digits=5, decimal_places=2)
    precio_total = serializers.DecimalField(min_value=1, max_digits=5, decimal_places=2)

class OrdenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orden
        fields = (
            'tienda',
            'fecha_de_entrega_usuario',
            'precio_total_orden'
        ) 



class OrdenSpecificSerializer(serializers.Serializer):
    tienda = serializers.IntegerField(min_value=1)
    fecha_de_entrega_usuario = serializers.DateField() #'2019-09-24', 
    precio_total_orden = serializers.DecimalField(min_value=1, max_digits=5, decimal_places=2)

    products = ItemSpecificSerializer(
        many=True,
        read_only=False
    )

    def validate_tienda(self, value):
        from tienda.models import Tienda
        from datetime import datetime as dt
        from datetime import date as dt_date

        respuesta_validacion = False
        tienda = Tienda.objects.get(id=value)
        #print("tienda ................ dias semana laborables windows")
        #print(tienda.dias_semana_horarios_laborales())

        if 'hoy' in self.context.keys(): # im sending artificial today, for testing purposes
            today = dt.strptime(self.context["hoy"], "%Y-%m-%d")
            today = today.date()
        else:
            today = dt_date.today()

        print("today ......................{}".format(today))

        if 'fecha_de_entrega_usuario' in self.context.keys(): 
            fecha_de_entrega_validation = dt.strptime(self.context["fecha_de_entrega_usuario"], "%Y-%m-%d")
            fecha_de_entrega_validation = fecha_de_entrega_validation.date()

            if 'products' in self.context.keys():
                products_json = self.context["products"]
                respuesta_validacion = tienda.validacion_en_horarios_laborales(today, fecha_de_entrega_validation, products_json)                
            if respuesta_validacion[0]:
                pass
            else:
                raise serializers.ValidationError("Lo sentimos, pero la tienda no puede entregar los productos en la fecha indicada: {} next_delivery_date {}".format(fecha_de_entrega_validation, respuesta_validacion[1]))

        return value

    def validate_fecha_de_entrega_usuario(self, data):
        from datetime import datetime as dt
        from datetime import date as dt_date

        if len(self.context) > 0: # im sending artificial today, for testing purposes
            today = dt.strptime(self.context["hoy"], "%Y-%m-%d")
            today = today.date()
        else:
            today = dt_date.today()

        '''
        print("context .......................")
        print(self.context)
        print("data.......................")
        print(data)
        print(type(data))
        print("...............today {}, value {}".format(today, data))
        '''

        if data < today:
            raise serializers.ValidationError("Cant buy in past")
        return data


    def create(self, validated_data):
        tienda = Tienda.objects.get(id=validated_data.get('tienda'))
        order = Orden.objects.create(
            tienda=tienda,
            fecha_de_entrega_usuario=validated_data.get('fecha_de_entrega_usuario'),
            precio_total_orden=validated_data.get('precio_total_orden')
            )
        productos_s = validated_data.get('products', [])
        for p in productos_s:
            cantidad        = p['cantidad']
            precio_unitario = p['precio_unitario']
            precio_total    = p['precio_total']

            p = Producto.objects.get(slug=p['slug'])
            Item.objects.create(
                orden=order, 
                producto=p, 
                cantidad=cantidad, 
                precio_unitario=precio_unitario, 
                precio_total=precio_total
                )
        return order