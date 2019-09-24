from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .models import *
from .serializers import *

class OrdenViewSet(viewsets.ViewSet):
    def create(self, request):
        dicc_context = {}
        today = self.request.query_params.get('today', None)
        if today: # artificial today
            dicc_context['hoy'] = today
        if 'fecha_de_entrega_usuario' in request.data.keys():
            dicc_context['fecha_de_entrega_usuario'] = request.data.get('fecha_de_entrega_usuario', None)
        if 'products' in request.data.keys():
            dicc_context['products'] = request.data.get('products', [])

        serializer = OrdenSpecificSerializer(data=request.data, context=dicc_context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)