"""commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from tienda import views as views_tienda
from productos import views as views_productos
from orden import views as views_orden

router = routers.DefaultRouter()
router.register(r'tiendas', views_tienda.TiendaViewSet)
router.register(r'productos', views_productos.ProductoViewSet)
router.register(r'checkout/orden/', views_orden.OrdenViewSet, basename="checkout")

urlpatterns = [
	path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
