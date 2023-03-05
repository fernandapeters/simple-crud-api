import uuid
import logging

from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, APIRouter

from . import crud
from . import schemas
from . import database


router = APIRouter()
logger = logging.getLogger(__name__)


def get_db():
    db = database.LocalSession()
    try:
        yield db
    finally:
        db.close()


@router.post("/products/", response_model=None)
def create_product(product: schemas.Product, request: Request, db: Session = Depends(get_db)):
    db_product_by_name = crud.get_product_by_name(db, product_name=product.name)

    if db_product_by_name:
        logger.warning(f"[{request.method}] Name {product.name} is already registered.")
        raise HTTPException(status_code=400, detail="Name is already registered")

    db_product_by_id = crud.get_product(db, product_id=product.id)
    if db_product_by_id:
        logger.warning(f"[{request.method}] Id {product.id} already exists.")
        raise HTTPException(status_code=400, detail="Id already exists")

    db_product = crud.create_product(db=db, product=product)
    if db_product is None:
        raise HTTPException(status_code=500, detail="Product could not be registered")

    return db_product


@router.get("/products/", response_model=List[schemas.Product])
def read_products(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    if products is None:
        raise HTTPException(404, "No products found")

    return products


@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id, request: Request, db: Session = Depends(get_db)):
    try:
        product = crud.get_product(db=db, product_id=uuid.UUID(product_id))
    except ValueError as e:
        logger.warning(f"Id ({product_id}) format is invalid. {e}")
        raise HTTPException(400, f"{product_id} is not a valid id")

    if product is None:
        logger.warning(f"[{request.method}] Product with id {product_id} does not exists.")
        raise HTTPException(404, f"Product with id {product_id} was not found")

    return product


@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id, request: Request, product: schemas.Product, db: Session = Depends(get_db)):
    product_updated = crud.update_product(db=db, product_id=product_id, product=product)
    if product_updated is None:
        logger.warning(f"[{request.method}] Product with id {product_id} could not be updated.")
        raise HTTPException(500, f"Product with id {product_id} could not be updated")

    return product_updated


@router.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id, request: Request, db: Session = Depends(get_db)):
    product_deleted = crud.delete_product(db=db, product_id=product_id)
    if product_deleted is None:
        logger.warning(f"[{request.method}] Product with id {product_id} could not be deleted.")
        raise HTTPException(500, f"Product with id {product_id} could not be deleted.")

    return product_deleted

