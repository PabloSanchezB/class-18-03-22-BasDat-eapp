from itertools import product
from unicodedata import name
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey #importamos todo lo necesario
#de sqlalchemy. OJO!! al "tipo de dato" Text
from sqlalchemy.orm import relationship #recordar que orm=object relational mapping. En este caso,
#.orm es un subpaquete de la libreria sqlalchemy
from database.session import Base #La Base de tipo declarativa que creamos en session.py


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True) #auto incrementa la primary key
    name = Column(String(55))
    product = relationship("Product", back_populates="category") #"Product": nombre de la clase
    #Product. "category": nombre de la relationship category que esta como atributo en la clase 
    #Product. Y lo mismo en reversa (ver category en Product). Notese que la relacion entre productos
    #y categorias es de uno a muchos: Un producto pertenece a solo una categoria, pero dentro de
    #una categoria hay varios productos

class Product(Base):
    __tablename__ = "products" #Una cosa es el nombre de la clase y otra el nombre de la tabla

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    quantity = Column(Integer)
    description = Column(Text) #OJO al tipo Text
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE")) #ondelete="CASCADE": Si
    #borro una categoria en la tabla "category", todos los productos asociados a esa categoria también
    #se borran 
    category = relationship("Category", back_populates="product")
    #order_details = relationship("OrderDetails", back_populates="product_order_details")
    #cart_items = relationship("CartItems", back_populates="products")