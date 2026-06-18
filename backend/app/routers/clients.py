from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.get("/")
def list_clients(
    db: Session = Depends(get_db)
):
    return db.query(Client).all()


@router.post("/")
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Client).filter(
        Client.cnpj == payload.cnpj
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="CNPJ já cadastrado"
        )

    client = Client(**payload.dict())

    db.add(client)
    db.commit()
    db.refresh(client)

    return client