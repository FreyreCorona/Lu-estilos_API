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
ProductCreate = sqlalchemy_to_pydantic(models.Product)
OrderCreate = sqlalchemy_to_pydantic(models.Order)
ImageCreae = sqlalchemy_to_pydantic(models.Image)
ProductOrderCreate = sqlalchemy_to_pydantic(models.ProductOrder)


