# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['id', 'nombre', 'tienda']
    list_filter = ['tienda']

admin.site.register(Producto, ProductoAdmin)