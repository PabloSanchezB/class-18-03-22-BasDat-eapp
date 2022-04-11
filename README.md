# Clase Viernes 18-03-22
## Implementación base de datos

[CLASE 0:47:00]

NOTA: Al clonar (bajar desde remoto) un repositorio, este se clona sin las dependencias instaladas. TOCA INSTALARLAS. Al trabajar con venv + pip y teniendo el entorno venv activado, el profe corrió el siguiente comando:

pip install -r .\requirements.txt

El equivalante al requirements.txt en poetry debe ser el poetry.lock, asi que el comando en poetry debe ser algo como:

poetry add -r .\poetry.lock

..... Pero no estoy seguro......

OJO!!!!! Recordar que database/session.py ha sido renombrado por el profe como db.py, pero aclearqui lo seguiremos llamando session.py OJO!!!!!

OJO!!!! Hay discrepancias entre el repo subido por el profe y lo de aqui.... discrepancias que no he visto al profe digitar en ninguna clase. Porsilasmoscas... solo voy a digitar aqui lo que el profe escriba EN CLASE. Si al final esto no funciona, significa que dichas discrepancias si eran necesarias despues de todo......

poetry add fastapi uvicorn[standard] SQLAlchemy alembic

Siguientes 2 lineas: Libs necesarias para poder instalar el psycopg2 (said libs already installed...)

sudo apt-get install libpq-dev python-dev

sudo apt-get install build-essential

poetry add psycopg2

cart, orders, products, y user son los modulos correspondientes a entidades (tablas) de la base de datos implementada. Puede haber mas de una tabla definida en cada modulo...

database: modulo para la base de datos

core: modulo para funcionalidades para toda la aplicación

core/config.py: donde configuramos como nos conectamos a la base de datos

database/session.py: donde creamos la sesión para establecer la conección con la base de datos. OJO!!! El profe ha renombrado este archivo como db.py, pero aqui lo seguiremos llamando session.py

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

database/models.py es un modulo de ayuda para que Alembic encuentre todos los modelos que estoy importando

MODELO DTO (Data Transfer Object)

products/services.py: El modulo de servicios, esa capa intermedia entre los modelos de tablas (de SQLAlchemy) y las APIS

products/router.py: El modulo de rutas (get, delete, post, update...). Aqui se definen los endpoints (URIs). Aqui cada funcion de ruta va a llamar a su correspondiente servicio creado en products/services.py

products/schema.py: Los esquemas de Pydantic. Permiten serializar o deserializar las peticiones hechas desde el cliente al API, convirtiendo JSONs a objetos Python y viceversa (objetos de retorno y entrada de las APIS)

products/validation.py: Para validaciones

Lo de arriba, junto con products/models.py representan la estructura de cualquier folder que guarde tablas
de base de datos, como en este caso son cart, orders y user.

Recordar que todas las rutas definidas en los diferentes router.py hay que importarlas en el main.py. El main.py es lo que se ejecuta cuando se corre el servidor uvicorn, lo que no este importado en el main.py es como si no existiera para el servidor.

Cuando el main.py ya este listo para probar:

OJO!!! Antes de correr el uvicorn hay que poner a correr el container de la base de datos (postgres)

poetry run uvicorn main:app --host 0.0.0.0 --port 8000

Tener en cuenta que al dar numeros de puertos demasiado bajos (84, por ejemplo), puede salir acceso denegado, por eso se recomienda siempre usar el puerto 8000

Cuando este corriendo el servidor ir en el browser a "localhost:8000/docs"

core/hashing.py: modulo para encriptar passwords. Requiere que instalemos los paquetes "passlib" y "argon2"

poetry add argon2-cffi

poetry add passlib[argon2]

Y tambien el validador de email:

poetry add pydantic[email]

SEGURIDAD Y TOKENS (https://fastapi.tiangolo.com/tutorial/security/first-steps/)

Necesitamos instalar las siguientes librerias: "python-multipart", "python-jose[cryptography]" (para encriptar y desencriptar tokens) y "passlib[bcrypt]" 

poetry add python-multipart

poetry add python-jose[cryptography]

poetry add passlib[bcrypt]

