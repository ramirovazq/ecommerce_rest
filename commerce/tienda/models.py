from django.db import models
from tienda.utils import lista_circular

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

    def dias_semana_horarios_laborales(self):
        answer = []
        for x in self.horarios_laborales():
            answer = answer + [y.valor for y in x.dias.all()]
        answer = list(set(answer)) # quito dias repetidos
        answer.sort()
        return answer

    def fecha_solicitada_dentro_de_dias_laborales(self, fecha_a_checar):
        answer = False
        for workingwindow in self.horarios_laborales():
            if fecha_a_checar.weekday() in workingwindow.dias_numeric(): # significa que cae dentro de un dia de los que se trabajan
                answer = True
                break
        return answer

    def next_posible_day(self, today, fecha_de_entrega_validation, dias_elaboracion):
        lista_dias_trabajo = self.dias_semana_horarios_laborales()
        dia_semana_que_pide = fecha_de_entrega_validation.weekday()
        #lista_circular(lista_dias_trabajo=[0, 1, 3, 4], dia_que_pide=5, dias_elaboracion=0, fecha=None):
        recomendation = lista_circular(lista_dias_trabajo, dia_semana_que_pide, dias_elaboracion, fecha_de_entrega_validation)
        return recomendation

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
        #print("recorriendo lista de productos ...............")
        list_answers = []
        list_recomendations = []
        list_products = self.json_products_list_objects(products_json)
        for producto in list_products:
            answer, recomendation = self.validacion_en_horarios_laborales_producto(today, fecha_de_entrega_validation, producto)
            list_answers.append(answer)
            list_recomendations.append(recomendation)

        #print("list_answers..............")
        #print(list_answers)

        return not(False in list_answers), list_recomendations

    def validacion_en_horarios_laborales_producto(self, today, fecha_de_entrega_validation, producto): #tienda.validacion_en_horarios_laborales(today, fecha_de_entrega_validation, products_json)
        '''
        recibe la fecha de hoy, 
        recibe la fecha de entrega enviada por el usuario
        recibe un producto
        '''
        #print("validando un solo producto ...............")
        answer = False
        recomendation = None
        # productos con tiempo de elaboracion igual a cero, y el dia en que se solicita

        answer = self.fecha_solicitada_dentro_de_dias_laborales(fecha_de_entrega_validation)
        if not(answer): # si no cae dentro de alguno de los dias laborales
            recomendation = self.next_posible_day(today, fecha_de_entrega_validation, producto.tiempo_de_elaboracion)

        return (answer, recomendation)

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