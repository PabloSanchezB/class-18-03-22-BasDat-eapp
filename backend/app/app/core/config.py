from pydantic import BaseSettings #Nos permite hacer configuración
from typing import Optional
from functools import lru_cache #Para hacer un cache de la configuración. Para que no cree una nueva 
#instancia de la configuracion cada vez que la llamemos (y asi gastar menos memoria)

class Settings(BaseSettings):
    #APP_ENV: str = 'dev'
    DATABASE_USERNAME: str = 'postgres' #para poder cambiarlo luego con variables de entorno
    DATABASE_PASSWORD: str = '123123'
    DATABASE_HOST: str = 'localhost' #La url (mas bien el host/server...) donde esta ubicada la BD
    DATABASE_NAME: str = 'mydb' #'myecapp'
    #TEST_DATABASE_NAME: str = 'myecapp'

    DATABASE_URI: str = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
    #La cadena de conección. OJO!! A como se formatea esa string usando los atributos de la clase...
    #SQLALCHEMY_DATABASE_URI: Optional[str] = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*5 #Cinco dias!!!!
    #Variable de entorno que especifica cuando van a expirar los tokens (EN MINUTOS)

    JWT_SECRET: str = "VmkJXRnRYH7HLBve9afg3uv4NmDE5M5PvhQ93RNYtbAzRM8dWuzcU89GxeJ6SZCxhNwFq79DhM"
    #Para el Secret (La firma particular del servidor, quien la tenga podrá generar tokens para este servidor)
    
    ALGORITHM: str = "HS512"
    #El algoritmo JWT (de encriptación) que usaremos
    #En la pagina oficial de jwt podemos ver los algoritmos soportados

    class Config: #clase interna para la configuración
        case_sensitive: bool = True #Es case sensitive
    
@lru_cache #Hace un caché de la funcion que esta debajo
def get_settings() -> Settings:
    return Settings()

settings = get_settings() #creamos una instancia de Settings por medio de la función de aquí arriba
#Ya cacheada...para que no ande creando nuevas instancias de Settings todo el tiempo