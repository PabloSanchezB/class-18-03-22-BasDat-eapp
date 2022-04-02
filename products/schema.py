from pydantic import BaseModel, constr #constr es para hacer restricciones

class CategoryBase(BaseModel):
    #Esta clase base no lleva el id, ya que el id es para guardar en la base de datos y eso no se define
    #aqui
    name: constr(min_length=2, max_length=50)
    #OJO a como se usa constr

#Clase para CREAR una categoria
class CategoryCreate(CategoryBase):
    pass
    #Esta clase no hace nada, solo hereda de CategoryBase. Esta clase es para darle semantica a 
    #nuestro codigo, para que sepa que esta recibiendo un objeto para crear, no un objeto base

#Clase para actualizar
class CategoryUpdate(CategoryBase):
    pass

#Clase para representar el objeto cuando se va a guardar en la base de datos
class CategoryInDBBase(CategoryBase):
    #Esta si es la que lleva el id (ademas de los atributos que hereda de CategoryBase)
    id: int
    #Esta clase interna de aqui abajo es para que los objetos no los tome como diccionarios sino
    #como objetos de Python (Pydantic?)
    class Config:
        orm_mode = True

#Estas son para que se entienda mejor el codigo... Si nos da igual como se vea el codigo entonces
#las unicas dos clases que son absolutamante necesarias son CategoryBase y CategoryInDBBase

class Category(CategoryInDBBase):
    pass

class CategoryInDB(CategoryInDBBase):
    pass



