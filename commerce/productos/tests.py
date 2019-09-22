import datetime

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .models import Producto


class ProductoCreationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # se crea la tienda
        tienda_data = {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }

        response = self.client.post(
                reverse('tienda-list'),
                tienda_data,
                format="json"
        )
        response_json = response.json()
        self.id_tienda = response_json['id']

        self.product_data = {
            'nombre': 'Superpower Giving Coding Coffee Mug',
            'tienda': self.id_tienda,
            'precio': 159.59
        }



    def test_producto_creation(self):
        """
        Creación simple de un producto, 
        POST nombre
        """

        response = self.client.post(
                reverse('producto-list'),
                self.product_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()



    def test_product_slug(self):
        """
        Verificación del slug creado en el producto
        POST nombre
        """

        response = self.client.post(
                reverse('producto-list'),
                self.product_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()
        self.assertEqual(response_json['slug'], 'superpower-giving-coding-coffee-mug')
        

    def test_product_repeat_creation(self):
        """
        Creación repetida de una tienda, 
        POST nombre
        """

        response = self.client.post(
                reverse('producto-list'),
                self.product_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
                reverse('producto-list'),
                self.product_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertNotEqual(response_json['slug'], 'tienda-de-martha-de-pasteles-caseros')


    def test_producto_creation_with_elaboration_time(self):
        """
        Creación simple de un producto con tiempo de elaboracion distinto a cero
        POST nombre
        """
        self.product_data['nombre'] = 'Pastel de Chocolate' 
        self.product_data['tiempo_de_elaboracion'] = 2 # 2 dias en la elaboracion

        response = self.client.post(
                reverse('producto-list'),
                self.product_data,
                format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertEqual(response_json['tiempo_de_elaboracion'], 2)


'''
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
'''