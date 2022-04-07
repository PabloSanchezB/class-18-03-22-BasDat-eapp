from typing import List, Optional #Del python 3.10 para arriba ya no es necesario importar estos tipos...

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models
from . import schema

#Crear nuevo usuario
async def new_user_register(user_in: schema.UserCreate, db_session: Session) -> models.User:
    new_user = models.User(name=user_in.name, email=user_in.email, password=user_in.password)
    #new_user = models.User(**user_in.dict())
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user) #Aqui en el refresh es donde se crea y se asigna el nuevo id
    return new_user

async def all_users(db_session: Session) -> List[models.User]:
    users = db_session.query(models.User).all()
    return users

#Aqui puede que no devuelva nada, por eso devuelve un Optional (supongo....)
async def get_user_by_id(user_id: int, db_session: Session) -> Optional[models.User]:
    user_info = db_session.query(models.User).get(user_id)
    #if not user_info:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return user_info

async def delete_user_by_id(user_id: int, db_session: Session):
    db_session.query(models.User).filter(models.User.id == user_id).delete()
    db_session.commit()