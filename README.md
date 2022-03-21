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

Correr (montar el contenedor) (y descargar) la imagen de postgres con Docker (todo otro contenedor de postgres tiene que estar detenido) (los nombres de las variables de entorno estan en la pagina de docker hub de postgres y los valores son los que estan en core/config.py) (si no se le agrega ninguna versión despues de imagen_a_descargar entonces descarga la ultima versión):

docker run --name my-db-postgresql -e POSTGRES_USER=postgres -e POSTGRES_DB=mydb -e POSTGRES_PASSWORD=123123 -p 5432:5432 -d postgres 

docker run --name container_name -e variable_de_entorno_1=valor -e variable_de_entorno_2=valor -p puerto_entrada:puerto_salida -d imagen_a_descargar:version_especifica 

Inicializar Alembic(esto creará nuevos directorios dentro del folder de la app):

poetry run alembic init alembic

Dentro del directorio alembic se iran guardando las versiones (directorio versions). El archivo que ahora nos interesa es alembic/env.py. Este es el archivo para hacer las migraciones. Una vez hayamos modificado el alembic/env.py, autogeneramos nuestro archivo de migración con el siguiente:

poetry run alembic revision --autogenerate

El comando de arriba generará el archivo alembic/versions/90ba271921e4_.py, en donde estara la descripción o "traducción alembic" de las tablas que definimos. Ej: las que definimos en products/models.py

Luego ejecutamos:

poetry run alembic upgrade head

La cual ejecutará la funcion upgrade en 90ba271921e4_.py y creara las tablas en la base de datos de postgres

