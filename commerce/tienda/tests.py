import datetime

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .models import Tienda


class TiendaTests(TestCase):

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