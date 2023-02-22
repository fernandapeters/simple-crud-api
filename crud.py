import uuid
from sqlalchemy.orm import Session

import models
import schemas


def get_product(db: Session, product_id: uuid.UUID):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.name == product_name).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.Product):
    id_ = schemas.Product.id if hasattr(schemas.Product, 'id') else uuid.uuid4()
    db_product = models.Product(id=id_, name=product.name, description=product.description,
                                price=product.price, stock=product.stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
