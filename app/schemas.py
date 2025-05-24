from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal


# === IMAGE ===
class ImageBase(BaseModel):
    name: str

class ImageCreate(ImageBase):
    data: bytes
    product_id: int

class ImageRead(ImageBase):
    id: int

    class Config:
        orm_mode = True


# === PRODUCT ===
class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    section: Optional[str]
    code_bar: Optional[str]
    categroy: Optional[str]
    initial_stock: Optional[int] = 0
    actual_stock: Optional[int] = 0
    due_date: Optional[str]
    price: Decimal

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    images: List[ImageRead] = []

    class Config:
        orm_mode = True


# === CLIENT ===
class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    role: Optional[str] = "user"

class ClientCreate(ClientBase):
    password: str

class ClientRead(ClientBase):
    id: int

    class Config:
        orm_mode = True


# === PRODUCT ORDER ===
class ProductOrderBase(BaseModel):
    product_id: int
    amount: int

class ProductOrderCreate(ProductOrderBase):
    order_id: int

class ProductOrderRead(ProductOrderBase):
    id: int
    product: ProductRead

    class Config:
        orm_mode = True


# === ORDER ===
class OrderBase(BaseModel):
    name: str
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    client_id: int
    products: List[ProductOrderCreate]

class OrderRead(OrderBase):
    id: int
    date: datetime
    client: ClientRead
    products: List[ProductOrderRead]

    class Config:
        orm_mode = True

class ClientLogin(BaseModel):
    email:str
    password:str
    

class Token(BaseModel):
    access_token:str
    token_type:str
    
