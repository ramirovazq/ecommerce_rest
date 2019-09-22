import datetime

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .models import Tienda, Dias, TiendaWorkingWindow


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
