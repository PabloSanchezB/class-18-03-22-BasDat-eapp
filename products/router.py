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

#Este api_router no deberia ir abajo de todo??? NO!!!!! Lo que va debajo de todo es el
#app.include_router(api_router), pero ese NO VA AQUI, va en el main.py, es decir, este archivo
#router.py debemos importarlo en el main (usando un apodo, ver el main.py), para asi poder
#accesar este api_router de aqui abajo. Osea, lo que quedaria en el main seria:
#app.include_router(product_router.api_router) 
api_router = APIRouter(tags=["Products"]) #El tags es para ponerle un nombre para la documentación
#Todos los metodos de ruta de aqui abajo apareceran bajo un letrero de "Products" al mostrar la documentacion
#en el browser al darle localhost:port_number/docs

@api_router.post("/products/category/", status_code=status.HTTP_201_CREATED)
#Notese que create_category retorna un Any y no un models.Category como cabria esperar...
#Notese donde se usa el Depends
#OJO!!! get_db_session en database/session.py esta devolviendo un GENERADOR, osea, que a pesar de ser una funcion,
#aqui no la invocamos "session.get_db_session()", tenemos que quitarle los parentesis: "session.get_db_session"
async def create_category(category_in: schema.CategoryCreate, db_session: Session = Depends(session.get_db_session)) -> Any:
    #Aqui abajo invocamos la funcion (servicio) correspondiente a esta ruta que creamos en 
    #services.py
    new_category= await services.create_new_category(category=category_in, db_session=db_session)
    return new_category

@api_router.get("/products/category/", response_model=List[schema.Category])
async def get_all_categories(db_session: Session = Depends(session.get_db_session)):
    return await services.get_all_categories(db_session)

@api_router.get("/products/category/{category_id}", response_model=schema.Category)
async def get_category_by_id(category_id:int, db_session: Session = Depends(session.get_db_session)):
    category= await services.get_category_by_id(category_id, db_session)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    return category

@api_router.delete("/products/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(category_id:int, db_session: Session = Depends(session.get_db_session)):
    #Antes de eliminar, hay que saber si está o no...
    category= await services.get_category_by_id(category_id, db_session)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid category ID")
    
    return await services.delete_category_by_id(category_id, db_session)
    #Pero delete_category_by_id no retorna nada????? Entonces?????

@api_router.post('/products/', status_code=status.HTTP_201_CREATED)
async def create_product(product_in: schema.ProductCreate, db_session: Session = Depends(session.get_db_session)):
    category = await validation.verify_category_exist(product_in.category_id, db_session)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="You have provided invalid category id."
        )

    product = await services.create_new_product(product=product_in, db_session=db_session)
    return product

@api_router.get('/products/', response_model=List[schema.Product])
async def get_all_products(db_session: Session = Depends(session.get_db_session)):
    return await services.get_all_products(db_session)