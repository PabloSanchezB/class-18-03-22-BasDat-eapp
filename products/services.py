from typing import List #Tipos de datos que necesitamos. Recordar que python 3.10 para arriba ya
#tiene muchos de estos tipos ya integrados sin necesidad de importarlos
from sqlalchemy.orm import Session
from . import models #El punto se refiere a la raiz en la que esta este mismo archivo, osea, aqui
#estamos importando products/models.py
from . import schema
#Aqui en services lo que se hace es convertir modelos de sqlalchemy a esquemas de pydantic y viceversa
#por eso importamos models,py y schema.py

#Funcion (servicio) para crear una nueva categoria. Recibe un objeto (esquema de pydantic) tipo 
#CategoryCreate (un objeto a crear) (parametro category) y una sesion de base de datos (parametro 
#db_session), y devuelve un modelo para tabla sqlAlchemy. OJO a como se usa la semantica de
#"CategoryCreate" y "Category"
async def create_new_category(category: schema.CategoryCreate, db_session: Session) -> models.Category:
    #db_category = models.Category(name=category.name) #Creamos una instancia de Category y le pasamos
    #los valores de sus campos por medio de atributos nombrados que vienen en el parametro category
    #Pero y si hay 10 atributos? Una forma de hacerlo rapido es la de abajo: convertimos category
    #en un diccionario y luego lo "desagregamos" con **
    db_category = models.Category(**category.dict())
    db_session.add(db_category) #A la sesion recibida como parametro se le agrega con add() el objeto
    #db_category (un modelo sqlAlchemy) que construimos arriba a partir del esquema de pydantic category
    #que recibio esta funcion como parametro
    db_session.commit() #Confirmamos la transaccion
    db_session.refresh(db_category) #Aqui es donde lo mete a la tabla y le asigna la id correspondiente
    return db_category

#Retorna una lista de modelos sqlalchemy Category
async def get_all_categories(db_session: Session) -> List[models.Category]:
    #.query() es para hacer consultas sql a la base de datos. Le pido que traiga un objeto Category
    #y .all() es para que traiga todos los que haya en la BD. Esto seria equivalente a un:
    # "SELECT * FROM category" (el nombre de la tabla es "category", ver en products/models.py)
    categories = db_session.query(models.Category).all()
    return categories

async def get_category_by_id(category_id:int, db_session:Session) -> models.Category:
    #.get("primary key number")
    #OJO!! "id" es el nombre del atributo de la clase (modelo) Category en products/models.py
    #          -------------------EN DUDA, NO ES CORRECTO LO DE ABAJO---------------
    #OJO!! Si el parametro de arriba "category_id" se llamara "id", igual que el atributo de la
    #clase Category, no habria que poner ".get(id=category_id)" sino solamente ".get(id)"
    #             ----------------EN DUDA, NO ES CORRECTO LO DE ARRIBA----------------
    #Ojo, al explicar lo de aqui arriba, el profe parece confundirse.... VIDEO CLASE 29/03/22 [0:52:00]
    #.get() recibe como parametro el numero del primary key del objeto a buscar, retorna UN (1) solo
    #objeto
    category = db_session.query(models.Category).get(category_id)
    return category

async def delete_category_by_id(category_id:int, db_session:Session): #No retorna nada
    #.filter("criterio de filtrado") funciona como un WHERE de sql. A diferencia de get(),
    #que solo devuelve un (1 objeto), filter() puede devolver varios. En este caso el filter()
    #esta devolviendo un (1) solo objeto, ya qu esta filtrando mediante una primary key...
    db_session.query(models.Category).filter(models.Category.id == category_id).delete()
    db_session.commit() #Siempre que se haga un cambio en los datos (insertar o eliminar), debemos
    #usar .commit()




