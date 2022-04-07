from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.session import Base
from core import hashing


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    #order = relationship("Order", back_populates="user_info")
    #cart = relationship("Cart", back_populates="user_cart")

    def __init__(self, name, email, password, *args, **kwargs):
        self.name = name
        self.email = email
        #Necesitamos encriptar el password
        self.password = hashing.get_password_hash(password) #Aqui genera la password encriptada
        #La encriptacion se hace dentro del constructor, para que cuando se instancie un nuevo objeto, de una se
        #encripte el password

    def check_password(self, password): #Verifica si el password que estoy pasando es igual al password guardado en
    #el objeto
        return hashing.verify_password(self.password, password)

