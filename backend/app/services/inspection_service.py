from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import (
    Project,
    InspectionAnswer,
    NonConformity
)


def validate_project_active(
    db: Session,
    project_id: int
):

    project = db.query(Project).get(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado"
        )

    if project.status.lower() != "ativo":
        raise HTTPException(
            status_code=400,
            detail="Inspeção permitida apenas em projetos ativos"
        )

    return project


def validate_answers(
    answers
):

    for answer in answers:

        if not answer.resposta:
            raise HTTPException(
                status_code=400,
                detail="Todas as respostas são obrigatórias"
            )


def save_answers(
    db: Session,
    inspection_id: int,
    answers
):

    for answer in answers:

        inspection_answer = InspectionAnswer(
            inspection_id=inspection_id,
            pergunta=answer.pergunta,
            resposta=answer.resposta,
            risco=answer.risco,
            evidencia=answer.evidencia
        )

        db.add(inspection_answer)

        # Gera NC automática
        if (
            answer.risco
            and answer.risco.lower()
            in ["alto", "crítico", "critica"]
        ):

            nc = NonConformity(
                inspection_id=inspection_id,
                origem="Inspeção",

                descricao=f"""
                Não conformidade automática:
                {answer.pergunta}
                """,

                severidade="crítica",

                status="aberta"
            )

            db.add(nc)

    db.commit()