from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate

from app.models import Project, Client
from app.schemas import ProjectCreate

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    client = db.query(Client).get(payload.client_id)

    if not client:
        raise HTTPException(404, "Cliente inválido")

    project = Project(**payload.dict())

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/")
def list_projects(status: str = "", db: Session = Depends(get_db)):
    query = db.query(Project)

    if status:
        query = query.filter(Project.status == status)

    return query.all()