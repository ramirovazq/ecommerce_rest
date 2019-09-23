import datetime

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

#from .models import Orden
from productos.models import *
from tienda.models import *


class OrdenCreationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # creacion de tienda
        tienda_data = {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }
        response = self.client.post(
                reverse('tienda-list'),
                tienda_data,
                format="json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # creacion de working window para tienda
        l = Dias.objects.create(valor=0, dia="Lunes")
        m = Dias.objects.create(valor=1, dia="Martes")        
        j =Dias.objects.create(valor=3, dia="Jueves")
        v =Dias.objects.create(valor=4, dia="Viernes")
        tienda = Tienda.objects.get(nombre=tienda_data
            ['nombre'])

        self.id_tienda = tienda.id

        tw_one = TiendaWorkingWindow.objects.create(
            tienda=tienda, 
            start_time="09:00",
            end_time="18:00"
            )
        tw_one.dias.add(l)
        tw_one.dias.add(m)
        tw_one.dias.add(j)
        tw_one.dias.add(v)

        # adicion de productos a la tienda
        self.product_data_uno = {
            'nombre': 'Superpower Giving Coding Coffee Mug',
            'tienda': self.id_tienda,
            'precio': 159.59,
            'tiempo_de_elaboracion': 2
        }
        response = self.client.post(
                reverse('producto-list'),
                self.product_data_uno,
                format="json"
        )
        response_json = response.json()
        self.product_data_uno_id = response_json['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.product_data_dos = {
            'nombre': 'Cosmic Machine Learning Healing Drops',
            'tienda': self.id_tienda,
            'precio': 359.59
            #'tiempo_de_elaboracion': 0
        }
        response = self.client.post(
                reverse('producto-list'),
                self.product_data_dos,
                format="json"
        )
        response_json = response.json()
        self.product_data_dos_id = response_json['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # today
        import datetime
        self.today = datetime.datetime(2019, 9, 24, 0, 0) # tuesday 24 sept 2019

        self.products_send_order = [{
                'slug': 'superpower-giving-coding-coffee-mug',
                'cantidad': 2,
                'precio_unitario': 100,
                'precio_total': 200
            },{
                "slug": "cosmic-machine-learning-healing-drops", 
                "cantidad": 1, 
                "precio_unitario": 350, 
                "precio_total": 350
                }]

        self.products_send_order_tiempo_elaboracion_zero = [{ 
                "slug": "cosmic-machine-learning-healing-drops", 
                "cantidad": 1, 
                "precio_unitario": 350, 
                "precio_total": 350
                }]


    '''
    def test_order__past_day__cant_buy(self):

        self.today = datetime.datetime(2019, 9, 29, 0, 0) # monday 29 sept 2019
        delivery_date = datetime.datetime(2019, 9, 20, 0, 0) # same day        

        order_price = 550

        order_data = {
            'products': self.products_send_order,
            'tienda': self.id_tienda,
            'fecha_de_entrega_usuario': delivery_date.strftime('%Y-%m-%d'),
            'precio_total_orden': order_price
        }

        response = self.client.post(
                reverse('checkout-list')+"?today="+self.today.strftime('%Y-%m-%d'),
                order_data,
                format="json"
        )
        response_json = response.json() 
        print(response_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    '''
    
    def test_order__zero_tiempo_elaboracion__want_same_day(self):

        self.today = datetime.datetime(2019, 9, 24, 0, 0) # tuesday 24 sept 2019
        delivery_date = datetime.datetime(2019, 9, 24, 0, 0) # same day        

        self.id_tienda
        order_price = 550

        order_data = {
            'products': self.products_send_order_tiempo_elaboracion_zero,
            'tienda': self.id_tienda,
            'fecha_de_entrega_usuario': delivery_date.strftime('%Y-%m-%d'),
            'precio_total_orden': order_price
        }

        response = self.client.post(
                reverse('checkout-list')+"?today="+self.today.strftime('%Y-%m-%d'),
                order_data,
                format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)