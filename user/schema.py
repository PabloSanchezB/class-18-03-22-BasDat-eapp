from pydantic import BaseModel, constr, validator, EmailStr 

class UserBase(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr #Tipo de dato EmailStr (tipo especial de string)

class UserCreate(UserBase):
    password: str #El password no se debe estar mostrando siempre, solo cuando se necesite,
    #por ejemplo, al crear (registrar) un nuevo usuario


#Este es para guardarlo en la BD
class UserInDBBase(UserBase):
    id: int
    password: str

    class Config:
        orm_mode = True

#Este es para traermelo de la BD (Ahi no necesito andar mostrando el password....)
class User(UserBase):
    id: int
    class Config:
        orm_mode = True

