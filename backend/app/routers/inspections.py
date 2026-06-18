from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    Inspection
)

from app.schemas import (
    InspectionCreate
)

from app.services.inspection_service import (
    validate_project_active,
    validate_answers,
    save_answers
)

router = APIRouter(
    prefix="/inspections",
    tags=["Inspections"]
)


@router.get("/")
def list_inspections(
    db: Session = Depends(get_db)
):
    return db.query(Inspection).all()


@router.post("/")
def create_inspection(
    payload: InspectionCreate,
    db: Session = Depends(get_db)
):

    # Valida projeto ativo
    validate_project_active(
        db,
        payload.project_id
    )

    # Valida respostas
    validate_answers(
        payload.answers
    )

    inspection = Inspection(
        client_id=payload.client_id,
        project_id=payload.project_id,
        checklist_id=payload.checklist_id,

        localizacao=payload.localizacao,

        assinatura=payload.assinatura,

        status="finalizada"
    )

    db.add(inspection)
    db.commit()
    db.refresh(inspection)

    # Salva respostas
    save_answers(
        db,
        inspection.id,
        payload.answers
    )

    return inspection