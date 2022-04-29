from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session #Aqui importamos la base de datos
from app.core.security import create_access_token
from app.database import session
from typing import Any
from app.user.services import authenticate

api_router = APIRouter(tags = ['Auth'])

@api_router.post("/login") #OJO!!!! Esta url "/login" es la misma que definimos en la linea 12 de core/security.py
#auth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
#"form_data" es la información del FORMULARIO
#¿por que el Depends() en "form_data:OAuth2PasswordRequestForm = Depends()" va sin nada dentro del parentesis???
#Depends es una clase de fastapi, toca ver en la documentación de fastapi que es lo que hace Depends. Segun el
#profe, lo esta "inyectando automaticamante".....
def login(db_session: Session = Depends(session.get_db_session), form_data:OAuth2PasswordRequestForm = Depends()) -> Any:
    #Nos traemos el usuario verificando email y contraseña 
    user = authenticate(email = form_data.username, password = form_data.password, db_session = db_session)
    if not user:
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")
    
    return {
        "access_token": create_access_token(sub = user.email),
        "token_type": "Bearer",
    }
