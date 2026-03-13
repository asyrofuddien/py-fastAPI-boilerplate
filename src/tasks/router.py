from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from . import schemas, service


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[schemas.TasksResponse])
def get_taskss(db: Session = Depends(get_db)):
    tasks_service = service.TasksService(db)
    return tasks_service.get_all()


@router.get("/{id}", response_model=schemas.TasksResponse)
def get_tasks(id: int, db: Session = Depends(get_db)):
    tasks_service = service.TasksService(db)
    tasks = tasks_service.get_by_id(id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks


@router.post("/", response_model=schemas.TasksResponse)
def create_tasks(data: schemas.TasksCreate, db: Session = Depends(get_db)):
    tasks_service = service.TasksService(db)
    return tasks_service.create(data)
