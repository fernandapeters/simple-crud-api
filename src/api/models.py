import uuid
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.dialects.postgresql import UUID

import database


class Product(database.Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    price = Column(DECIMAL(10, 2))
    stock = Column(Integer)
