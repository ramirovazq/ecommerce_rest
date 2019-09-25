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




## Corre las pruebas y observalo funcionando

Arranca el proyecto

```
(ecommerce-env) usuario@tu-maquina:~$ python3 manage.py test
```


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

