import uuid
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from . import models
from . import schemas


logger = logging.getLogger(__name__)


def get_product(db: Session, product_id: uuid.UUID):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.name == product_name).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.Product) -> bool:
    id_ = product.id if product.id is not None else uuid.uuid4()
    logger.info(f"Registering product {product.name} with id {id_}.")

    db_product = models.Product(id=id_, name=product.name, description=product.description,
                                price=product.price, stock=product.stock)
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    except SQLAlchemyError as e:
        logger.error(str(e.__dict__['orig']))
        return False

    return True


def delete_product(db: Session, product_id: uuid.UUID):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    try:
        db.delete(db_product)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(str(e.__dict__['orig']))
        return None

    return db_product


def update_product(db: Session, product: schemas.Product, product_id: uuid.UUID):
    db_query = db.query(models.Product).filter(models.Product.id == product_id)
    try:
        db_query.update(product.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(str(e.__dict__['orig']))
        return None
    return db_query.first()

