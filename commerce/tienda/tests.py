from datetime import timedelta as t_delta
import datetime

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .models import Tienda, Dias, TiendaWorkingWindow

from datetime import timedelta

def next_weekday(d, weekday):
    import datetime
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def lista_circular(dias_trabajo=[0, 1, 3, 4], dia_que_pide=5, dias_elaboracion=0, fecha=None):
    '''
    devuelve el dia de la semana siguiente en laborar
    '''
    from itertools import cycle
    dias_semana = list(range(7)) # [0,1,2,3,4,5,6]
    pool = cycle(dias_semana)
    # se posiciona en el dia base
    for x in range(dia_que_pide+1):
        indice_final = next(pool)
    #fecha_en_que_pide es el dia base inicial
    while True:
        if indice_final not in dias_trabajo:
            indice_final = next(pool)
        else:
            break
    if fecha:
        fecha = next_weekday(fecha, indice_final)
    pool_dias_trabajo = cycle(dias_trabajo)
    # se posiciona en el dia de trabajo en que se quedó indice_final
    for x in range(len(dias_trabajo)):
        dia_trabajo = next(pool_dias_trabajo)
        if indice_final == dia_trabajo:
            break
    # avanzo el numero de dias de elaboracion, sobre la lista de dias_trabajo
    for x in range(dias_elaboracion):
        indice_final = next(pool_dias_trabajo)
        if fecha:
            fecha = next_weekday(fecha, indice_final)

    if not fecha:
        return indice_final
    else:
        return (indice_final, fecha)

class CircularListWeekTests(TestCase):

    def setUp(self):
        self.list_weekdays = [3, 4] # jueves, y viernes
        self.fecha = datetime.datetime(2109,9,24) # solicita el martes 24 sept

    def test_cero_petition(self, dia=2, dias_elaboracion=0):#se pide en miercoles osea 2
        dia_semana, fecha_propuesta = lista_circular(self.list_weekdays, dia, dias_elaboracion, self.fecha)
        self.assertEqual(dia_semana, 3)#jueves
        self.assertEqual(fecha_propuesta, datetime.datetime(2109,9,26))#26sep


    def test_uno_petition(self, dia=2, dias_elaboracion=1):#se pide en miercoles osea 2
        dia_semana, fecha_propuesta = lista_circular(self.list_weekdays, dia, dias_elaboracion, self.fecha)
        self.assertEqual(dia_semana, 4)#viernes
        self.assertEqual(fecha_propuesta, datetime.datetime(2109,9,27))#27sep

    def test_dos_petition(self, dia=2, dias_elaboracion=2):
        dia_semana, fecha_propuesta =  lista_circular(self.list_weekdays, dia, dias_elaboracion, self.fecha)
        #self.assertEqual(res, 3)
        self.assertEqual(dia_semana, 3)#jueves
        self.assertEqual(fecha_propuesta, datetime.datetime(2109,10,3))#3 oct


    def test_tres_petition(self, dia=2, dias_elaboracion=3):
        dia_semana, fecha_propuesta = lista_circular(self.list_weekdays, dia, dias_elaboracion, self.fecha)
        #self.assertEqual(res, 4)
        self.assertEqual(dia_semana, 4)#viernes
        self.assertEqual(fecha_propuesta, datetime.datetime(2109,10,4))#4 oct



    def test_cuatro_petition(self, dia=2, dias_elaboracion=4):
        dia_semana, fecha_propuesta = lista_circular(self.list_weekdays, dia, dias_elaboracion, self.fecha)
        #self.assertEqual(res, 3)
        self.assertEqual(dia_semana, 3)#jueves
        self.assertEqual(fecha_propuesta, datetime.datetime(2109,10,10))#10 oct

    def test_cuatro_petition(self, dia=2, dias_elaboracion=5):
        dia_semana, fecha_propuesta = lista_circular(self.list_weekdays, dia, dias_elaboracion, self.fecha)
        #self.assertEqual(res, 3)
        self.assertEqual(dia_semana, 4)#viernes
        self.assertEqual(fecha_propuesta, datetime.datetime(2109,10,11))#11 oct
    



class CircularListZeroTests(TestCase):

    def setUp(self):
        self.list_weekdays = [0, 1, 3, 4] # monday, tuesday, thursday, friday

    def test_miercoles_petition(self, dia=2, dias_elaboracion=1):
        res = lista_circular(self.list_weekdays, dia, dias_elaboracion)
        self.assertEqual(res, 4)

    def test_miercoles_petition_two(self, dia=2, dias_elaboracion=2):
        res = lista_circular(self.list_weekdays, dia, dias_elaboracion)
        self.assertEqual(res, 0)

    def test_miercoles_petition_three(self, dia=2, dias_elaboracion=3):
        res = lista_circular(self.list_weekdays, dia, dias_elaboracion)
        self.assertEqual(res, 1)

    def test_miercoles_petition_four(self, dia=2, dias_elaboracion=4):
        res = lista_circular(self.list_weekdays, dia, dias_elaboracion)
        self.assertEqual(res, 3)

    def test_miercoles_petition_five(self, dia=2, dias_elaboracion=5):
        res = lista_circular(self.list_weekdays, dia, dias_elaboracion)
        self.assertEqual(res, 4)


class CircularListOneTests(TestCase):

    def setUp(self):
        self.list_weekdays = [0, 1, 3, 4] # monday, tuesday, thursday, friday

    def test_monday_petition(self, dia=0):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 0)

    def test_tuesday_petition(self, dia=1):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 1)

    def test_wednesday_petition(self, dia=2):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 3)

    def test_thursday_petition(self, dia=3):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 3)

    def test_friday_petition(self, dia=4):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 4)

    def test_saturday_petition(self, dia=5):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 0)

    def test_sunday_petition(self, dia=6):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 0)



class CircularListTwoTests(TestCase):

    def setUp(self):
        self.list_weekdays = [0, 1, 3] # lunes, martes, jueves

    def test_miercoles_petition(self, dia=2):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 3)

    def test_jueves_petition(self, dia=3):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 3)

    def test_viernes_petition(self, dia=4):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 0)

    def test_sabado_petition(self, dia=5):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 0)

    def test_domingo_petition(self, dia=6):
        res = lista_circular(self.list_weekdays, dia)
        self.assertEqual(res, 0)



class TiendaCreationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tienda_data = {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }


    def test_tienda_creation(self):
        """
        Creación simple de una tienda, 
        POST nombre
        """

        response = self.client.post(
                reverse('tienda-list'),
                self.tienda_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_verification_slug(self):
        """
        Verificación del slug creado en la tienda
        POST nombre
        """

        response = self.client.post(
                reverse('tienda-list'),
                self.tienda_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()
        self.assertEqual(response_json['slug'], 'tienda-de-martha-de-pasteles-caseros')
        

    def test_tienda_repeat_creation(self):
        """
        Creación repetida de una tienda, 
        POST nombre
        """

        response = self.client.post(
                reverse('tienda-list'),
                self.tienda_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
                reverse('tienda-list'),
                self.tienda_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertNotEqual(response_json['slug'], 'tienda-de-martha-de-pasteles-caseros')


class ObtainTiendaTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        tienda_data = {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }
        response = self.client.post(
                reverse('tienda-list'),
                tienda_data,
                format="json"
            )
        l = Dias.objects.create(valor=0, dia="Lunes")
        m = Dias.objects.create(valor=1, dia="Martes")
        mi = Dias.objects.create(valor=2, dia="Miércoles")
        j =Dias.objects.create(valor=3, dia="Jueves")
        v =Dias.objects.create(valor=4, dia="Viernes")
        s =Dias.objects.create(valor=5, dia="Sábado")
        d =Dias.objects.create(valor=6, dia="Domingo")

        tienda = Tienda.objects.get(nombre=tienda_data['nombre'])

        tw_one = TiendaWorkingWindow.objects.create(
            tienda=tienda, 
            start_time="09:00",
            end_time="18:00"
            )
        tw_one.dias.add(l)
        tw_one.dias.add(m)
        tw_one.dias.add(mi)
        tw_one.dias.add(j)
        tw_one.dias.add(v)

        tw_two = TiendaWorkingWindow.objects.create(
            tienda=tienda, 
            start_time="09:00",
            end_time="18:00"
            )
        tw_two.dias.add(s)

    def test_obtain_tienda(self):
        """
        Se obtiene GET de una tienda, 
        que tiene horarios de trabajo
        """

        response = self.client.get(
                reverse('tienda-list'),
                format="json"
        )

        response_json = response.json()
        self.assertEqual(len(response_json[0]['store_schedules']), 2) # se agregaron 2 working windows



class TiendaCreationVariousTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tienda_uno_data = {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }
        response = self.client.post(
                reverse('tienda-list'),
                self.tienda_uno_data,
                format="json"
        )
        

        self.tienda_dos_data = {
            'nombre': 'Tienda de Artesanias Mexicanas',
        }
        self.slug_tienda_dos ='tienda-de-artesanias-mexicanas'

        response = self.client.post(
                reverse('tienda-list'),
                self.tienda_dos_data,
                format="json"
        )
        response_json = response.json()
        self.tienda_dos_id = response_json['id']


    def test_get_specific_tienda(self):
        """
        Obtención simple de una tienda, 
        POST nombre
        """
        response = self.client.get(
                reverse('tienda-detail', kwargs={'slug':self.slug_tienda_dos}),
                format="json"
        )
        response_json= response.json()
        self.assertEqual(len(response_json), 4) # 4 elements, from one strore



class TiendaCreationAddingProductsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tienda_uno_data = {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }
        response = self.client.post(
                reverse('tienda-list'),
                self.tienda_uno_data,
                format="json"
        )

        response_json = response.json()
        self.id_tienda = response_json['id']
        self.slug_tienda = response_json['slug']

        self.product_data = {
            'nombre': 'Suavizante para la Ropa',
            'tienda': self.id_tienda,
            'precio': 159.59
        }
        response = self.client.post(
                reverse('producto-list'),
                self.product_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.product_data = {
            'nombre': 'Pastel de Chocolate',
            'tienda': self.id_tienda,
            'precio': 399.99
        }
        response = self.client.post(
                reverse('producto-list'),
                self.product_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        


    def test_get_specific_tienda_products(self):
        """
        Obtención de los productos de una tienda, 
        POST nombre
        """
        response = self.client.get(
                reverse('tienda-productos', kwargs={'slug':self.slug_tienda}),
                format="json"
        )
        response_json= response.json()
        self.assertEqual(len(response_json), 2) # 2 products from one strore
