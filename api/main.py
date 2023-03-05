import uuid
import time
import random
import string
import uvicorn
import logging

from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Request

from . import crud
from . import schemas
from . import database


logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.LocalSession()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status code={response.status_code}")

    return response


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(e)
        if isinstance(e, HTTPException):
            raise e


@app.post("/products/", response_model=None)
def create_product(product: schemas.Product, request: Request, db: Session = Depends(get_db)):
    db_product_by_name = crud.get_product_by_name(db, product_name=product.name)

    if db_product_by_name:
        logger.warning(f"[{request.method}] Name {product.name} is already registered.")
        raise HTTPException(status_code=400, detail="Name is already registered")

    db_product_by_id = crud.get_product(db, product_id=product.id)
    if db_product_by_id:
        logger.warning(f"[{request.method}] Id {product.id} already exists.")
        raise HTTPException(status_code=400, detail="Id already exists")

    success = crud.create_product(db=db, product=product)
    if success is False:
        raise HTTPException(status_code=500, detail="Product could not be registered")

    return success


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    if products is None:
        raise HTTPException(404, "No products found")

    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
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


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id, request: Request, product: schemas.Product, db: Session = Depends(get_db)):
    product_updated = crud.update_product(db=db, product_id=product_id, product=product)
    if product_updated is None:
        logger.warning(f"[{request.method}] Product with id {product_id} could not be updated.")
        raise HTTPException(500, f"Product with id {product_id} could not be updated")

    return product_updated


@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id, request: Request, db: Session = Depends(get_db)):
    product_deleted = crud.delete_product(db=db, product_id=product_id)
    if product_deleted is None:
        logger.warning(f"[{request.method}] Product with id {product_id} could not be deleted.")
        raise HTTPException(500, f"Product with id {product_id} could not be deleted.")

    return product_deleted


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
