from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from . import schemas, service


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[schemas.ProductsResponse])
def get_productss(db: Session = Depends(get_db)):
    products_service = service.ProductsService(db)
    return products_service.get_all()


@router.get("/{id}", response_model=schemas.ProductsResponse)
def get_products(id: int, db: Session = Depends(get_db)):
    products_service = service.ProductsService(db)
    products = products_service.get_by_id(id)
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    return products


@router.post("/", response_model=schemas.ProductsResponse)
def create_products(data: schemas.ProductsCreate, db: Session = Depends(get_db)):
    products_service = service.ProductsService(db)
    return products_service.create(data)
