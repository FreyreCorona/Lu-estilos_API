from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import app.models as models 

#GET Schemas
Client = sqlalchemy_to_pydantic(models.Client)
Product = sqlalchemy_to_pydantic(models.Product)
Order = sqlalchemy_to_pydantic(models.Order)
Image = sqlalchemy_to_pydantic(models.Image)
ProductOrder = sqlalchemy_to_pydantic(models.ProductOrder)

#POST Schemas
ClientCreate = sqlalchemy_to_pydantic(models.Client,exclude=['id'])
ProductCreate = sqlalchemy_to_pydantic(models.Product,exclude=['id'])
OrderCreate = sqlalchemy_to_pydantic(models.Order,exclude=['id'])
ImageCreae = sqlalchemy_to_pydantic(models.Image,exclude=['id'])
ProductOrderCreate = sqlalchemy_to_pydantic(models.ProductOrder,exclude=['id'])

class ClientLogin(BaseModel):
    email:str
    password:str
    

class Token(BaseModel):
    access_token:str
    token_type:str
    
