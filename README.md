# Clase Viernes 18-03-22
## Implementación base de datos

poetry add fastapi uvicorn[standard] SQLAlchemy alembic

Siguientes 2 lineas: Libs necesarias para poder instalar el psycopg2 (said libs already installed...)

sudo apt-get install libpq-dev python-dev

sudo apt-get install build-essential

poetry add psycopg2

cart, orders, products, y user son los modulos correspondientes a entidades (tablas) de la base de datos implementada. Puede haber mas de una tabla definida en cada modulo...


