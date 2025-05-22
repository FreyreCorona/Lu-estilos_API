from .database import Base 
from sqlalchemy import Column,Integer,String

class Table_base(Base):
    __abstract__ = True
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String)

class User(Table_base):
    __abstract__ = True

    email = Column(String)
    password = Column(String)

class Product(Table_base):
    __tablename__:str = "products"

    description = Column(String)
    price = Column(Integer)

class Client(User):
    __tablename__:str = "clients"
 
class Staff(User):
    __tablename__ = "staff"
    role = Column(String)
