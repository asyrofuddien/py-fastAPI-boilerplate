from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


class TasksService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[models.Tasks]:
        return self.db.query(models.Tasks).all()

    def get_by_id(self, id: int) -> Optional[models.Tasks]:
        return self.db.query(models.Tasks).filter(models.Tasks.id == id).first()

    def create(self, data: schemas.TasksCreate) -> models.Tasks:
        db_obj = models.Tasks(**data.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
