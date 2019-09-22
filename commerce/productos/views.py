from django.shortcuts import render
from django.utils.text import slugify

from rest_framework import viewsets

from .models import Producto
from tienda.utils import unique_slug
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Producto.objects.all().order_by('-id')
    serializer_class = ProductoSerializer

    def __save_slug(self, serializer, producto):
        producto_name  = slugify(producto.nombre)
        if producto_name:
            posible_slug = "{}".format(producto_name)
            if posible_slug: # must be not empty
                slug = unique_slug(posible_slug, Producto)
                producto.slug = slug
                producto.save()
            return producto

    def perform_create(self, serializer):
        producto = serializer.save()
        self.__save_slug(serializer, producto)