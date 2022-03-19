from sqlalchemy import create_engine #Para crear el motor de concección
from sqlalchemy.ext.declarative import declarative_base #vamos a hacer una conección tipo declarativa
from sqlalchemy.orm import sessionmaker #El que se encarga de crear la sesión
from core.config import settings #importamos el objeto settings (la instancia cacheada de la clase 
#Settings)

engine = create_engine(settings.DATABASE_URI) #creamos el motor que crea la conección a la BD
#recibe como parametro la URI de la BD

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Esta sesión local la va
#a hacer conectandose a la BD cuyo motor de conección y URI recibió como argumento en el parametro bind 
#(bind=engine)

Base = declarative_base() #creamos la Base como de tipo declarativa