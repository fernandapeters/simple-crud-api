import uuid

from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    description: str
    price: float
    stock: int

    class Config:
        orm_mode = True
