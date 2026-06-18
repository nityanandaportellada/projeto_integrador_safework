from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate

from app.models import NonConformity, NCAction
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(
    prefix="/nc",
    tags=["Non Conformities"]
)


# =========================
# SCHEMAS
# =========================

class NCActionCreate(BaseModel):
    descricao: str
    responsavel: str
    prazo: Optional[datetime] = None
    status: str = "pendente"


class NonConformityCreate(BaseModel):
    inspection_id: Optional[int] = None
    origem: str
    descricao: str
    severidade: str
    prazo: Optional[datetime] = None
    status: str = "aberta"
    responsavel: Optional[str] = None
    actions: List[NCActionCreate] = []


class NonConformityUpdate(BaseModel):
    origem: Optional[str] = None
    descricao: Optional[str] = None
    severidade: Optional[str] = None
    prazo: Optional[datetime] = None
    status: Optional[str] = None
    responsavel: Optional[str] = None


# =========================
# CREATE NC
# =========================

@router.post("/")
def create_nc(
    payload: NonConformityCreate,
    db: Session = Depends(get_db)
):
    nc = NonConformity(
        inspection_id=payload.inspection_id,
        origem=payload.origem,
        descricao=payload.descricao,
        severidade=payload.severidade.lower(),
        prazo=payload.prazo,
        status=payload.status,
        responsavel=payload.responsavel
    )

    db.add(nc)
    db.commit()
    db.refresh(nc)

    # Criação do plano de ação
    for action in payload.actions:
        action_item = NCAction(
            nc_id=nc.id,
            descricao=action.descricao,
            responsavel=action.responsavel,
            prazo=action.prazo,
            status=action.status
        )

        db.add(action_item)

    db.commit()

    return {
        "message": "Não conformidade criada com sucesso",
        "nc": nc,
        "alerta": (
            "AÇÃO IMEDIATA NECESSÁRIA"
            if nc.severidade == "crítica"
            else None
        )
    }


# =========================
# LIST NC
# =========================

@router.get("/")
def list_nc(
    severidade: str = "",
    status: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(NonConformity)

    if severidade:
        query = query.filter(
            NonConformity.severidade == severidade.lower()
        )

    if status:
        query = query.filter(
            NonConformity.status == status.lower()
        )

    ncs = query.order_by(
        NonConformity.id.desc()
    ).all()

    return ncs


# =========================
# GET NC
# =========================

@router.get("/{nc_id}")
def get_nc(
    nc_id: int,
    db: Session = Depends(get_db)
):
    nc = db.query(NonConformity).get(nc_id)

    if not nc:
        raise HTTPException(
            status_code=404,
            detail="Não conformidade não encontrada"
        )

    actions = db.query(NCAction).filter(
        NCAction.nc_id == nc.id
    ).all()

    return {
        "nc": nc,
        "actions": actions
    }


# =========================
# UPDATE NC
# =========================

@router.put("/{nc_id}")
def update_nc(
    nc_id: int,
    payload: NonConformityUpdate,
    db: Session = Depends(get_db)
):
    nc = db.query(NonConformity).get(nc_id)

    if not nc:
        raise HTTPException(
            status_code=404,
            detail="Não conformidade não encontrada"
        )

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(nc, key, value)

    db.commit()
    db.refresh(nc)

    return {
        "message": "NC atualizada com sucesso",
        "nc": nc
    }


# =========================
# DELETE NC
# =========================

@router.delete("/{nc_id}")
def delete_nc(
    nc_id: int,
    db: Session = Depends(get_db)
):
    nc = db.query(NonConformity).get(nc_id)

    if not nc:
        raise HTTPException(
            status_code=404,
            detail="Não conformidade não encontrada"
        )

    # Remove ações vinculadas
    db.query(NCAction).filter(
        NCAction.nc_id == nc.id
    ).delete()

    db.delete(nc)
    db.commit()

    return {
        "message": "NC removida com sucesso"
    }


# =========================
# ADD ACTION PLAN
# =========================

@router.post("/{nc_id}/actions")
def add_action(
    nc_id: int,
    payload: NCActionCreate,
    db: Session = Depends(get_db)
):
    nc = db.query(NonConformity).get(nc_id)

    if not nc:
        raise HTTPException(
            status_code=404,
            detail="NC não encontrada"
        )

    action = NCAction(
        nc_id=nc.id,
        descricao=payload.descricao,
        responsavel=payload.responsavel,
        prazo=payload.prazo,
        status=payload.status
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    return {
        "message": "Plano de ação criado",
        "action": action
    }


# =========================
# LIST ACTIONS
# =========================

@router.get("/{nc_id}/actions")
def list_actions(
    nc_id: int,
    db: Session = Depends(get_db)
):
    actions = db.query(NCAction).filter(
        NCAction.nc_id == nc_id
    ).all()

    return actions