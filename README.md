# Clase Viernes 18-03-22
## Implementación base de datos [1:23:00]

poetry add fastapi uvicorn[standard] SQLAlchemy alembic

Siguientes 2 lineas: Libs necesarias para poder instalar el psycopg2 (said libs already installed...)

sudo apt-get install libpq-dev python-dev

sudo apt-get install build-essential

poetry add psycopg2

cart, orders, products, y user son los modulos correspondientes a entidades (tablas) de la base de datos implementada. Puede haber mas de una tabla definida en cada modulo...

database: modulo para la base de datos

core: modulo para funcionalidades para toda la aplicación

core/config.py: donde configuramos como nos conectamos a la base de datos

database/session.py: donde creamos la sesión para establecer la conección con la base de datos

Correr (montar el contenedor) (y descargar) la imagen de postgres con Docker (todo otro contenedor de postgres tiene que estar detenido):

docker run --name my-db-postgresql -e POSTGRES_USER=postgres -e POSTGRES_DB=mydb -e POSTGRES_PASSWORD=123123 -p 5432:5432 -d postgres 

docker run --name container_name -e variable_de_entorno_1=valor -e variable_de_entorno_2=valor -p puerto_entrada:puerto_salida -d imagen_a_descargar:version_especifica 


