from django.core.exceptions import MultipleObjectsReturned
from datetime import timedelta as t_delta

import datetime
import random

def next_weekday(d, weekday):
    import datetime
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def lista_circular(dias_trabajo=[0, 1, 3, 4], dia_que_pide=5, dias_elaboracion=0, fecha=None):
    # dias_trabajo, son los dias de la semana en que trabajan 0 lunes; 1 martes; 2 miercoles ...
    # dia_que_pide, es el dia de la seman en que hace la solicitud
    # dias_elaboracion, es el numero de dias en que se elabora el producto
    # fecha. es la fecha en que se hace la solicitud
    '''
    devuelve el dia de la semana siguiente en laborar
    '''
    from itertools import cycle
    dias_semana = list(range(7)) # [0,1,2,3,4,5,6]
    pool = cycle(dias_semana)
    # se posiciona en el dia base
    for x in range(dia_que_pide+1):
        indice_final = next(pool)
    #fecha_en_que_pide es el dia base inicial
    while True:
        if indice_final not in dias_trabajo:
            indice_final = next(pool)
        else:
            break
    if fecha:
        fecha = next_weekday(fecha, indice_final)
    pool_dias_trabajo = cycle(dias_trabajo)
    # se posiciona en el dia de trabajo en que se quedó indice_final
    for x in range(len(dias_trabajo)):
        dia_trabajo = next(pool_dias_trabajo)
        if indice_final == dia_trabajo:
            break
    # avanzo el numero de dias de elaboracion, sobre la lista de dias_trabajo
    for x in range(dias_elaboracion):
        indice_final = next(pool_dias_trabajo)
        if fecha:
            fecha = next_weekday(fecha, indice_final)

    if not fecha:
        return indice_final
    else:
        return (indice_final, fecha)


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