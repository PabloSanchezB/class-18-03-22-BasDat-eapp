from typing import List, Optional #Del python 3.10 para arriba ya no es necesario importar estos tipos...

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models
from . import schema
from core import hashing

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

async def update_user_by_id(user_id:int, user: schema.UserUpdate, db_session:Session):
    hashed = hashing.get_password_hash(user.password)
    user.password = hashed
    db_session.query(models.User).filter(models.User.id == user_id).update(user.dict())
    db_session.commit()

#Por que esta de aqui abajo no es async??????
#OJO!!! Devuelve un Optional[] porque puede que no devuelva nada (no se encontró usuario con dicho email
#o la contraseña es incorrecta....)
def authenticate(*, email:str, password:str, db_session:Session) -> Optional[models.User]:
    user = db_session.query(models.User).filter(models.User.email == email).first()
    #first(): que nos retorne solo el primero que encuentre

    if not user:
        return None

    if not hashing.verify_password(password, user.password):
        return None
    
    return user
    

