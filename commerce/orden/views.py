from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .models import *
from .serializers import *

class OrdenViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = OrdenSpecificSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)