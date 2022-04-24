from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
#OAuth2PasswordBearer: El metodo de autenticación
from typing import List
from datetime import datetime, timedelta #Para los tiempos de expiración de los tokens
from sqlalchemy.orm import Session
from jose import jwt
from core.config import settings
from user.models import User
from database import session #database/session.py
from auth import schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login") #Instanciamos y le pasamos la url donde estoy haciendo el 
#login para generar el token. En este caso es "login", pero igual podria ser "/auth/login" o cualquier otra. 
#Pero OJO!!! Cuando cree el endpoint de ese url, este tiene que tener ese mismo nombre que he especificado aqui.

def create_access_token(*, sub:str) -> str:
    return _create_token(token_type = "access_token", lifetime = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES), sub = sub)
#"lifetime" es el tiempo de vida del token
#"sub" es la informacion que queremos mandarle

#Esta de aqui abajo es la funcion que esta siendo invocada en el return de la funcion de arriba
def _create_token(token_type:str, lifetime:timedelta, sub:str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime #utcnow() retorna la fecha y hora actuales
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow() #Que significa "iat"??????
    payload["sub"] = str(sub) #¿Por que este casteo a string?????
    return jwt.encode(payload, settings.JWT_SECRET, algorithm = settings.ALGORITHM)
#El payload es una de las 3 partes que conforman el token, junto con el header y la firma (ver diapos)
#settings.JWT_SECRET seri la firma. ¿Entonces settings.ALGORITHM seria el header?????

#Funcion para obtener el usuario
async def get_current_user(db_session: Session = Depends(session.get_db_session), token: str = Depends(oauth2_scheme)) -> User: #from user.models import User
    #Asi es!!! Una excepcion se puede guardar en una variable
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"}) #Que metodo de autenticación

    try:
        #Nos traemos el payload
        payload = jwt.decode(
            token, #El token
            settings.JWT_SECRET, #La firma
            algorithms=[settings.ALGORITHM], #El algoritmo que utilizamos
            options={"verify_aud":False},
        )

        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception

    user = db_session.query(User).filter(User.email == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user






