from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    Inspection,
    InspectionAnswer
)

from app.services.pdf_service import (
    generate_inspection_pdf
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/{inspection_id}")
def generate_report(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    inspection = db.query(Inspection).get(
        inspection_id
    )

    if not inspection:
        raise HTTPException(
            status_code=404,
            detail="Inspeção não encontrada"
        )

    answers = db.query(
        InspectionAnswer
    ).filter(
        InspectionAnswer.inspection_id
        == inspection_id
    ).all()

    report_path = generate_inspection_pdf(
        inspection,
        answers
    )

    return FileResponse(
        report_path,
        media_type="text/html",
        filename=f"inspection_{inspection_id}.html"
    )