from django.core.exceptions import MultipleObjectsReturned
from .models import Tienda
import random

def unique_slug(posible_slug, clase):
    unique = False
    try:
        clase.objects.get(slug=posible_slug)
        unique = False
    except clase.DoesNotExist:
        unique = True
    except MultipleObjectsReturned:
        unique = False

    if unique == False:
        return unique_slug("{}-{}".format(posible_slug, random.randint(1,101)), clase)
    else:
        return posible_slug