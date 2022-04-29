from typing import Any, List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from app.database import session

from . import schema
from . import services
from . import validation

api_router = APIRouter(
    tags=['Users']
)


#OJO!!! Si nosotros en esta función no especificamos un response_model, la función devolvera el usuario
#tal cual esta guardado en la base de datos, es decir, lo devolverá con todo y contraseña, aunque esta, por
#supuesto aparecerá encriptada. Si no queremos que aparezca, le decimos que el response_model sea
#schema.User, el cual no incluye la contraseña.
@api_router.post('/user/', status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_user_registration(user_in: schema.UserCreate, db_session: Session = Depends(session.get_db_session)):
    # Read More : Pydantic Validation with Database (https://github.com/tiangolo/fastapi/issues/979)

    user = await validation.verify_email_exist(user_in.email, db_session)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    new_user = await services.new_user_register(user_in, db_session)
    return new_user

@api_router.get('/user/', response_model=List[schema.User])
async def get_all_users(db_session: Session = Depends(session.get_db_session)):
    return await services.all_users(db_session)

@api_router.get('/user/{user_id}', response_model=schema.User)
async def get_user_by_id(user_id: int, db_session: Session = Depends(session.get_db_session)):
    return await services.get_user_by_id(user_id, db_session)

@api_router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id:int, db_session: Session = Depends(session.get_db_session)):
    user= await services.get_user_by_id(user_id, db_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")
    
    return await services.delete_user_by_id(user_id, db_session)

@api_router.put("/user/{user_id}", response_model = schema.User)
async def update_user_by_id(user_id:int, user_in: schema.UserUpdate, db_session: Session = Depends(session.get_db_session)) -> Any:
    user= await services.get_user_by_id(user_id, db_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")
    
    user2 = await validation.verify_email_exist(user_in.email, db_session)
    if user2 and user2.id != user_id:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    await services.update_user_by_id(user_id, user_in, db_session)

    return await services.get_user_by_id(user_id, db_session)