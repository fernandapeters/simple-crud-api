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


@app.post("/product/", response_model=None)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
