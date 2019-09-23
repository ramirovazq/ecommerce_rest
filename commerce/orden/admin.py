# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class OrdenAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['id', 'fecha_de_entrega_usuario', 'precio_total_orden', 'tienda']
    list_filter = ['tienda']

class ItemAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['id', 'orden', 'producto']


admin.site.register(Orden, OrdenAdmin)
admin.site.register(Item, ItemAdmin)