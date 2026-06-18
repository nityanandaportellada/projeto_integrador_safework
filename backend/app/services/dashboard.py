from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate

from app.models import Inspection, NonConformity

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    inspections = db.query(Inspection).count()

    open_nc = db.query(NonConformity).filter(
        NonConformity.status != "resolvida"
    ).count()

    critical_nc = db.query(NonConformity).filter(
        NonConformity.severidade == "crítica"
    ).all()

    return {
        "total_inspections": inspections,
        "open_nc": open_nc,
        "critical_nc": critical_nc
    }