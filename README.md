# Clase Viernes 18-03-22
## Implementación base de datos

video clase 0:59:00

REPO DEL PROFE:
https://github.com/jjpizarro/ec-app

PLANTILLA DE TIANGOLO:
https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D

OJO!! Tener en cuenta la estructura de carpetas cada vez que le demos comandos de consola que generen nuevos archivos, como por ejemplo "poetry run alembic init alembic" o "poetry init", para que asi los archivos generados queden dentro de las carpetas en que tienen que quedar...

OJO!!! Hemos modificado los directorios para que quedaran con la misma estructura del repo del profe y de la plantilla de tiangolo. Debido a la posicion en que ha quedado el main.py, a la hora de correr el uvicorn, debe hacerse como:

poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

NOTA: Al clonar (bajar desde remoto) un repositorio, este se clona sin las dependencias instaladas. TOCA INSTALARLAS. Al trabajar con venv + pip y teniendo el entorno venv activado, el profe corrió el siguiente comando:

pip install -r .\requirements.txt

El equivalante al requirements.txt en poetry debe ser el poetry.lock, asi que el comando en poetry debe ser algo como:

poetry add -r .\poetry.lock

..... Pero no estoy seguro......

OJO!!!!! Recordar que database/session.py ha sido renombrado por el profe como db.py, pero aclearqui lo seguiremos llamando session.py OJO!!!!!

OJO!!!! Hay discrepancias entre el repo subido por el profe y lo de aqui.... discrepancias que no he visto al profe digitar en ninguna clase. Porsilasmoscas... solo voy a digitar aqui lo que el profe escriba EN CLASE. Si al final esto no funciona, significa que dichas discrepancias si eran necesarias despues de todo......

Dentro de development creamos la carpeta del proyecto usando mkdir. Nos movemos dentro de la carpeta recien creada y checkeamos la version local de python con "pyenv versions" y "python -V". Le damos la estructura necesaria y le damos "git init" ("generará el oculto ".git") y "poetry init" (generará "pyproject.toml") en el fichero que corresponda. Creamos el repo remoto, seguimos las instrucciones "...or create a new repository on the command line", y luego de conectar a remoto y haber hecho el primer commit a remoto, nos ubicamos en donde este el pyproject.toml y le damos: 

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

products/services.py: El modulo de servicios, esa capa intermedia entre los modelos de tablas (de SQLAlchemy) y las APIS. Es donde va "la logica del negocio"

products/router.py: El modulo de rutas (get, delete, post, update...). Aqui se definen los endpoints (URIs). Aqui cada funcion de ruta va a llamar a su correspondiente servicio creado en products/services.py

products/schema.py: Los esquemas de Pydantic. Permiten serializar o deserializar las peticiones hechas desde el cliente al API, convirtiendo JSONs a objetos Python y viceversa (objetos de retorno y entrada de las APIS)

products/validation.py: Para validaciones

Lo de arriba, junto con products/models.py representan la estructura de cualquier folder que guarde tablas
de base de datos, como en este caso son cart, orders y user.

Recordar que todas las rutas definidas en los diferentes router.py hay que importarlas en el main.py. El main.py es lo que se ejecuta cuando se corre el servidor uvicorn, lo que no este importado en el main.py es como si no existiera para el servidor.

Cuando el main.py ya este listo para probar:

OJO!!! Antes de correr el uvicorn hay que poner a correr el container de la base de datos (postgres)

poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

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

Despues vamos al core/config.py y agregamos las variables de entorno necesarias para la seguridad. Para el JWT_SECRET nos vamos a https://passwordsgenerator.net/ y generamos un password de, digamos, 74 caracteres.... De-seleccionamos "include symbols" y le damos generate password. La copiamos y la usamos para JWT_SECRET (podemos modificarla o extenderla aun mas si queremos.....) 

Creamos core/security.py

Luego creamos el modulo/directorio auth y dentro de el auth/router.py. Aqui es donde crearemos nuestro login, que no es mas que una funcion de ruta de metodo post. Tambien creamos el servicio correspondiente en (OJO!!!!!) user/services.py

NOTA: "Auth" viene de "Authorization"

Luego importamos el respectivo router en el main.py

Ahora hay que darle seguridad a los endpoints que queramos proteger. Para esto tenemos que hacer que los endpoint a proteger sean dependientes de tener el usuario logeado. 

OJO!!! Aparentemente ES OBLIGATORIO llamar "current_user" al parametro que recibe al usuario logeado en cada uno de los endpoint que queramos proteger....

En la pagina de JWT, nosotros podemos pegar un token generado y la pagina lo decodifica. Lo que mas nos interesa es lo que esta en el sub, que en el caso de esta app de aqui, es el email del usuario. (Estudiar el codigo para que veamos como es que el email del usuario queda metido al fin en el sub del token...)

Para poder insertar el token en el header de la petición, tenemos que usar postman. El mtoken se ingresa con la clave "Authorization" y con el valor [tipo de token] [string del token]. En nuestro caso seria "Bearer [string del token]". Al pegar un body, tenemos que especificar que es JSON. 

DOCKER E IMAGENES

OJO!!! Se recomienda usar las versiones -slim de python: No pesan tanto como las completas pero tampoco son tan raquiticas como las -alpine....

Para crear nuestro Dockerfile nos basamos en esta documentación:
https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

OJO!!! Antes de crear la imagen, debemos desinstalar el psycopg2, ya que generará u error al crear la imagen:

poetry remove psycopg2

Y luego debems instalar:

poetry add psycopg2-binary

OJO!!! La desinstalacion e instalacion anteriores YA SE HICIERON EN ESTA APP!!!!!

Para construir la imagen: Estando ubicados en donde esta el Dockerfile:

docker build -t [nombre-de-mi-imagen] .

OJO!!!! Al puntico al final!!!

Para ver lista de imagenes: docker image ls

Para borrar una imagen: docker image rm [primeros-4-digitos-del-image-id]
Para ver los image id ver la lista de las imagenes

Aqui hay buena documentacion:
https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

Para correr nuestra imagen:
docker run -d --name [mycontainer] -p 80:80 [myimage]

El primer 80 es el puerto del equipo. El segundo 80 es el puerto del contenedor.
Cuando este corriendo, en el browser: localhost:80/docs
Nota: el 80 es el puerto por defecto, asi que no hay necesidad de ponerlo, podemos darle: localhost/docs

NOTESE que 2 contenedores corriendom al mismo tiempo no pueden acceder el uno al otro a menos que esten conectados por una red, pero hacer una red es trabajoso, es mas facil y rapido hacer un docker-compose: