from django.shortcuts import render
from django.utils.text import slugify

from rest_framework import viewsets

from .models import Tienda
from .utils import unique_slug
from .serializers import TiendaSerializer

class TiendaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Tienda.objects.all().order_by('-id')
    serializer_class = TiendaSerializer

    def __save_slug(self, serializer, tienda):
        tienda_name       = slugify(tienda.nombre)
        if tienda_name:
            posible_slug = "{}".format(tienda_name)
            if posible_slug: # must be not empty
                slug = unique_slug(posible_slug, Tienda)
                tienda.slug = slug
                tienda.save()
            return tienda

    def perform_create(self, serializer):
        tienda = serializer.save()
        self.__save_slug(serializer, tienda)    