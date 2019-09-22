from rest_framework import serializers
from .models import Tienda, Dias, TiendaWorkingWindow

class DiasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dias
        fields = (
            'dia',
        ) 

class TiendaWorkingWindowSerializer(serializers.ModelSerializer):
    dias = DiasSerializer(        
        required=False, 
        many=True
    )

    class Meta:
        model = TiendaWorkingWindow
        fields = (
            'dias', 
            'start_time',
            'end_time'
        ) 

class TiendaSerializer(serializers.ModelSerializer):
    store_schedules = serializers.SerializerMethodField()

    def get_store_schedules(self, obj):        
        schedules = TiendaWorkingWindow.objects.filter(tienda=obj)
        tienda_working_window_serializer = TiendaWorkingWindowSerializer(schedules, many=True)
        return tienda_working_window_serializer.data

    class Meta:
        model = Tienda
        fields = (
            'id',
            'nombre', 
            'slug',
            'store_schedules'
        ) 