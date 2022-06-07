# Api Beitech
## _Repositorio para el examen practico de programacion en python_
____

Se desea realizar ajuste sobre un sistema que permite realizar órdenes de productos para clientes.

## Desarrollo

El proyecto fue desarrollado usando Flask, Flask_SQLAlchemy, MySQL.

## Esquema de tablas

![alt text](https://github.com/mauricioPallares/beitech/blob/d51e2e05628fa5f00af839fade3db07fbe96acee/diagrama%20tablas.png)

### Modificaciones

-  Elimine el campo product_description de la tabla order_detail

## Crearcion del servicio web REST

Para la creacion del api se uso la extesion flask_restful y su documentacion fue hecha con Postman y se puede visualizar en el siguiente link.

  - [Doc Postman](https://documenter.getpostman.com/view/12900848/Uz5JHatw)


## Start

Luego de descargar el repositorio, se configura en al archivo /app/config.py la base de datos 

```
DB = {
    'host': "localhost",
    'user': "root",
    'passwd': "",
    'database': "ordenes",
}
```

para ejecutar la aplicacion se debe definir la variable de entorno FLASK_APP

```sh
export FLASK_APP=app
$ flask run
```


Al momento de ejecutarla por primera vez se generan las tablas en la base de datos.
En el archivo database.sql estan los datos de ejemplo para las tablas customer, product y customer_has_product.
