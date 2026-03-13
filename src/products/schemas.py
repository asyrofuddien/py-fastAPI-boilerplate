from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductsBase(BaseModel):
    pass


class ProductsCreate(ProductsBase):
    pass


class ProductsUpdate(ProductsBase):
    pass


class ProductsResponse(ProductsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
