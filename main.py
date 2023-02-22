import uuid

import uvicorn
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import database


database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.LocalSession()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=None)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product_by_name = crud.get_product_by_name(db, product_name=product.name)

    if db_product_by_name:
        raise HTTPException(status_code=400, detail="Name already registered")

    db_product_by_id = crud.get_product(db, product_id=product.id)
    if db_product_by_id:
        raise HTTPException(status_code=400, detail="Id already exists")

    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id, db: Session = Depends(get_db)):
    product = crud.get_product(db=db, product_id=uuid.UUID(product_id))
    if product is None:
        raise HTTPException(404, f"Product with id {product_id} does not exists")
    return product


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
