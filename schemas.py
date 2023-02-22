import uuid

from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: Optional[uuid.UUID]
    name: str
    description: str
    price: float
    stock: int

    class Config:
        orm_mode = True
