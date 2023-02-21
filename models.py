import uuid
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID

import database


class Product(database.Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
                # server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
