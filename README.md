# E-commerce Basic using REST

Productos, Tienda y Ordenes

## Getting Started

Este proyecto es la estructura basica de un e-commerce, utiliza la db (SQL) sqlite3. Está desarrollando usando Django 2.2.5, y Django Rest Framework 3.10.3

### Prerequisitos

Es necesario tener:

```
virtualenv
python3
```

### Instalación

Genera un nuevo ambiente virtual y actívalo.

```
usuario@tu-maquina:~/virtualenvs$ virtualenv -p python3 ecommerce-env
usuario@tu-maquina:~/virtualenvs$ $ source ecommerce-env/bin/activate
```

Descarga el proyecto

```
(ecommerce-env) usuario@tu-maquina:~/virtualenvs$ cd
(ecommerce-env) usuario@tu-maquina:~$ git clone https://github.com/ramirovazq/ecommerce_rest.git

```

Entra al proyecto e instala los requirements.txt

```
(ecommerce-env) usuario@tu-maquina:~$ cd ecommerce_rest/commerce/
(ecommerce-env) usuario@tu-maquina:~$ pip3 install -r requirements.txt 

```

Arranca el proyecto

```
(ecommerce-env) usuario@tu-maquina:~$ python3 manage.py migrate
(ecommerce-env) usuario@tu-maquina:~$ python3 manage.py runserver

```




## Corre las pruebas 

Corre todas las pruebas escritas

```
(ecommerce-env) usuario@tu-maquina:~$ python3 manage.py test
```
Cada app del proyecto (orden, productos, tienda) tiene dentro un archivo tests.py, en ese archivo vienen las pruebas de funcionamiento acordes al documento del ejercicio.


## Observalo funcionando

Los pasos si se desea ver el proyecto funcionando (levanta el servidor de pruebas)

Para crear una tienda, haz un POST hacia http://127.0.0.1:8000/api/tiendas/

```
       {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }
```
Para adicionar los dias en que trabaja la tienda
```
$ ./manage.py carga_inicial_dias
```
Crea un super usuario
```
$ ./manage.py createsuperuser
```
Entra al proyecto desde el admin: http://127.0.0.1:8000/admin/tienda/tiendaworkingwindow/add/
Ahí se puede crear un horario para una tienda.


Para obtener los datos de una tienda, haz un GET hacia GET http://127.0.0.1:8000/api/tiendas/tienda-de-martha-de-pasteles-caseros/

```
       {
            'nombre': 'Tienda de Martha de pasteles Caseros',
        }
```



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

