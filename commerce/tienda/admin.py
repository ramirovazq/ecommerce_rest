# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Tienda

class TiendaAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['id', 'nombre', 'slug']
    list_filter = ['nombre']

admin.site.register(Tienda, TiendaAdmin)