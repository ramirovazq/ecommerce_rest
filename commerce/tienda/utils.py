from django.core.exceptions import MultipleObjectsReturned
from .models import Tienda
import random

def unique_slug(posible_slug):
    unique = False
    try:
        Tienda.objects.get(slug=posible_slug)
        unique = False
    except Tienda.DoesNotExist:
        unique = True
    except MultipleObjectsReturned:
        unique = False

    if unique == False:
        return unique_slug("{}-{}".format(posible_slug, random.randint(1,101)))
    else:
        return posible_slug