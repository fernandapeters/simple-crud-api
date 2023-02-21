import uuid

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

    class Config:
        orm_mode = True
