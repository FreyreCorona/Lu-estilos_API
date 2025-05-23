from sqlalchemy.orm import relationship
from .database import Base 
from sqlalchemy import Column, DateTime,Integer, LargeBinary,String,Text,Numeric,ForeignKey
from datetime import datetime


class Table_base(Base):
    __abstract__ = True
    id = Column(Integer,primary_key=True)
    name = Column(String(length=200))

class Client(Table_base):
    __tablename__ = "clients"
    
    email = Column(String(length=50),unique=True)
    password = Column(String(length=100))
    role = Column(String(length=50))

    order = relationship("Order",back_populates="client")

class Product(Table_base):
    __tablename__:str = "products"

    description = Column(Text)
    section = Column(String)
    code_bar = Column(String(length=50))
    categroy= Column(String)
    initial_stock =Column(Integer)
    actual_stock = Column(Integer,default=0)
    due_date = Column(String)
    price = Column(Numeric(10,2))

    images = relationship("Image",back_populates="product",cascade="all,delete-orphan")

class Image(Table_base):
    __tablename__ = "images"

    data = Column(LargeBinary)
    product_id = Column(Integer,ForeignKey("products.id"))

    product = relationship("Product",back_populates="images")

class Order(Table_base):
    __tablename__:str = "orders"
    
    client_id = Column(Integer,ForeignKey("clients.id"))
    date = Column(DateTime,default=datetime.now())
    status = Column(String(length=50))

    client = relationship("Client",back_populates="order")
    products = relationship("ProductOrder",back_populates="order",cascade="all,delete")

class ProductOrder(Base):
    id = Column(Integer,primary_key=True)
    order_id = Column(Integer,ForeignKey("order.id"))
    product_id = Column(Integer,ForeignKey("products.id"))
    amount = Column(Integer,nullable=False)

    order = relationship("Order",back_populates="products")
    product = relationship("Product")
    
