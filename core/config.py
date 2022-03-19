from pydantic import BaseSettings #Nos permite hacer configuración
from typing import Optional
from functools import lru_cache #Para hacer un cache de la configuración. Para que no cree una nueva 
#instancia de la configuracion cada vez que la llamemos (y asi gastar menos memoria)

class Settings(BaseSettings):
    DATABASE_USERNAME: str = 'postgres' #para poder cambiarlo luego con variables de entorno
    DATABASE_PASSWORD: str = '123123'
    DATABASE_HOST: str = 'localhost' #La url (mas bien el host/server...) donde esta ubicada la BD
    DATABASE_NAME: str = 'mydb'

    DATABASE_URI: str = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
    #La cadena de conección. OJO!! A como se formatea esa string usando los atributos de la clase...

    class Config: #clase interna para la configuración
        case_sensitive: bool = True #Es case sensitive
    
@lru_cache #Hace un caché de la funcion que esta debajo
def get_settings() -> Settings:
    return Settings()

settings = get_settings() #creamos una instancia de Settings por medio de la función de aquí arriba
#Ya cacheada...para que no ande creando nuevas instancias de Settings todo el tiempo