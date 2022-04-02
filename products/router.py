from fastapi import APIRouter, Depends, status, Response, HTTPException
#Depends: Para hacer inyeccion de dependencia de la coneccion a la base de datos. Depende de que vaya
#y traiga esa coneccion
#status: para poder colocar los nombres de los status http en vez de poner numeros
#Response: Para las respuestas
from sqlalchemy.orm import Session
from typing import Any, List
from database import session #database/session.py
from . import schema
from . import services
from . import validation

#Este api_router no deberia ir abajo de todo???
api_router = APIRouter(tags=["Products"]) #El tags es para ponerle un nombre para la documentación

@api_router.post("/products/category/", status_code=status.HTTP_201_CREATE)
#Notese que create_category retorna un Any y no un models.Category como cabria esperar...
#Notese donde se usa el Depends
async def create_category(category_in: schema.CategoryCreate, db_session: Session = Depends(session.get_db_session())) -> Any:
    #Aqui abajo invocamos la funcion (servicio) correspondiente a esta ruta que creamos en 
    #services.py
    new_category= await services.create_new_category(category=category_in, db_session=db_session)
    return new_category

@api_router.get("/products/category/", response_model=List[schema.Category])
async def get_all_categories(db_session: Session = Depends(session.get_db_session())):
    return await services.get_all_categories(db_session)

@api_router.get("/products/category/{category_id}", response_model=schema.Category)
async def get_category_by_id(category_id:int, db_session: Session = Depends(session.get_db_session())):
    category= await services.get_category_by_id(category_id, db_session)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    return category

@api_router.delete("/products/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(category_id:int, db_session: Session = Depends(session.get_db_session())):
    #Antes de eliminar, hay que saber si está o no...
    category= await services.get_category_by_id(category_id, db_session)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid category ID")
    
    return await services.delete_category_by_id(category_id, db_session)
    #Pero delete_category_by_id no retorna nada????? Entonces?????