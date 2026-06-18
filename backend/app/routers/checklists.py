from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate
from app.models import Checklist, ChecklistQuestion
from app.schemas import ChecklistCreate

router = APIRouter(prefix="/checklists", tags=["Checklists"])


@router.post("/")
def create_checklist(payload: ChecklistCreate, db: Session = Depends(get_db)):
    checklist = Checklist(nome=payload.nome)

    db.add(checklist)
    db.commit()
    db.refresh(checklist)

    for q in payload.questions:
        question = ChecklistQuestion(
            checklist_id=checklist.id,
            pergunta=q.pergunta,
            tipo=q.tipo,
            obrigatoria=q.obrigatoria,
            exige_evidencia=q.exige_evidencia
        )

        db.add(question)

    db.commit()

    return checklist


@router.post("/{checklist_id}/version")
def create_version(checklist_id: int, db: Session = Depends(get_db)):
    original = db.query(Checklist).get(checklist_id)

    if not original:
        raise HTTPException(404, "Checklist não encontrado")

    original.bloqueado = True

    new_checklist = Checklist(
        nome=original.nome,
        versao=original.versao + 1
    )

    db.add(new_checklist)
    db.commit()

    return new_checklist