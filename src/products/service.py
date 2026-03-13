from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


class ProductsService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[models.Products]:
        return self.db.query(models.Products).all()

    def get_by_id(self, id: int) -> Optional[models.Products]:
        return self.db.query(models.Products).filter(models.Products.id == id).first()

    def create(self, data: schemas.ProductsCreate) -> models.Products:
        db_obj = models.Products(**data.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
