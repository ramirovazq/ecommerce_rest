# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Tienda, Dias, TiendaWorkingWindow

class TiendaAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['id', 'nombre', 'slug']

class DiasAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['id', 'valor', 'dia']


class TiendaWorkingWindowAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['id', 'tienda', 'start_time', 'end_time']

admin.site.register(Tienda, TiendaAdmin)
admin.site.register(Dias, DiasAdmin)
admin.site.register(TiendaWorkingWindow, TiendaWorkingWindowAdmin)