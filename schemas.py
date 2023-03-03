import uuid

from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    description: str
    price: float
    stock: int

    class Config:
        orm_mode = True
