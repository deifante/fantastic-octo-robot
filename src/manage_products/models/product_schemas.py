import datetime
from typing import Optional

from pydantic.main import BaseModel


# Shared properties
class ProductBase(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = ""


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    name: str
    price: float
    description: Optional[str] = ""


class ProductInDBBase(ProductBase):
    id: Optional[int] = None
    views: Optional[int] = None
    is_deleted: bool = False
    created_date: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Product(ProductInDBBase):
    id: int
    views: int
