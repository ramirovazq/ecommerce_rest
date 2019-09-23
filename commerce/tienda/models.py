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

    def mis_productos(self):
        from productos.models import Producto
        return Producto.objects.filter(tienda=self)

    def horarios_laborales(self):
        return TiendaWorkingWindow.objects.filter(tienda=self)

    def fecha_solicitada_dentro_de_horarios_laborales(self, fecha_a_checar):
        answer = False
        for workingwindow in self.horarios_laborales():
            print("--------------")
            print("dia fecha_a_checar {}".format(fecha_a_checar.weekday()))
            print("----dias_numeric----------")
            print(workingwindow.dias_numeric())
            if fecha_a_checar.weekday() in workingwindow.dias_numeric(): # significa que cae dentro de un dia de los que se trabajan
                answer = True
                break
        return answer


    def json_products_list_objects(self, list_of_dicts):
        from productos.models import Producto
        l = []
        for dictionary in list_of_dicts:
            p = Producto.objects.get(slug=dictionary['slug'])
            l.append(p)
        return l

    def validacion_en_horarios_laborales(self, today, fecha_de_entrega_validation, products_json): #tienda.validacion_en_horarios_laborales(today, fecha_de_entrega_validation, products_json)
        '''
        recibe la fecha de hoy, 
        recibe la fecha de entrega enviada por el usuario
        recibe el json de los productos
        '''
        print("recorriendo lista de productos ...............")
        list_answers = []
        list_products = self.json_products_list_objects(products_json)
        for producto in list_products:
            answer = self.validacion_en_horarios_laborales_producto(today, fecha_de_entrega_validation, producto)
            list_answers.append(answer)

        print("list_answers..............")
        print(list_answers)

        return not(False in list_answers)

    def validacion_en_horarios_laborales_producto(self, today, fecha_de_entrega_validation, producto): #tienda.validacion_en_horarios_laborales(today, fecha_de_entrega_validation, products_json)
        '''
        recibe la fecha de hoy, 
        recibe la fecha de entrega enviada por el usuario
        recibe un producto
        '''
        print("validando un solo producto ...............")
        answer = False
        # productos con tiempo de elaboracion igual a cero, y el dia en que se solicita
        if (producto.tiempo_de_elaboracion == 0):
            answer = self.fecha_solicitada_dentro_de_horarios_laborales(fecha_de_entrega_validation)
        return answer

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

    def dias_numeric(self):
        return [x[0] for x in self.dias.all().values_list('valor')]