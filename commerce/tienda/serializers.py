from rest_framework import serializers
from .models import Tienda

class TiendaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tienda
        fields = (
        	'nombre', 
        	'slug'
        ) 