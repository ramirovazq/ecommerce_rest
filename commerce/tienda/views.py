from django.shortcuts import render
from django.utils.text import slugify

from rest_framework.decorators import action
from rest_framework.response import Response
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
    lookup_field = 'slug'

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

    #@detail_route()
    @action(detail=True, methods=['get'])
    def productos(self, request, slug=None):
        from productos.serializers import ProductoSerializer

        tienda = self.get_object()
        productos = tienda.mis_productos()

        productos_ser = ProductoSerializer(productos, many=True)
        return Response(productos_ser.data)