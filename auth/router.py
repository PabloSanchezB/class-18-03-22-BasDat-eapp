from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.security import create_access_token
from database import session
from typing import Any
from user.services import authenticate

api_router = APIRouter(tags = ['Auth'])

@api_router.post("/login")
def login(db_session: Session = Depends(session.get_db_session), form_data:OAuth2PasswordRequestForm = Depends()) -> Any:
    user = authenticate(email = form_data.username, password = form_data.password, db_session = db_session)
    if not user:
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")
    
    return {
        "access_token": create_access_token(sub = user.mail),
        "token_type": "Bearer",
    }
