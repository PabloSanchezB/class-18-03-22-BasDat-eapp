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

auth2_scheme = OAuth2PasswordBearer(tokenUrl = "login") #Instanciamos y le pasamos la url donde estoy haciendo el 
#login para generar el token. En este caso es "login", pero igual podria ser "/auth/login" o cualquier otra. 
#Pero OJO!!! Cuando cree el endpoint de ese url, este tiene que tener ese mismo nombre que he especificado aqui.

def create_access_token(*, sub:str) -> str:
    return _create_token(token_type = "access_token", lifetime = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES), sub = sub)

def _create_token(token_type:str, lifetime:timedelta, sub:str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)
    return jwt.ecode(payload, settings.JWT_SECRET, algorithm = settings.ALGORITHM)




