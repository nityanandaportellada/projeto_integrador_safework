from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# =========================
# CLIENTS
# =========================

class ClientBase(BaseModel):
    nome: str
    cnpj: str

    endereco: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

    cnae: Optional[str] = None
    grau_risco: Optional[str] = None

    numero_funcionarios: Optional[int] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# PROJECTS
# =========================

class ProjectBase(BaseModel):
    client_id: int

    nome: str
    descricao: Optional[str] = None

    status: str = "ativo"

    responsavel: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# CHECKLISTS
# =========================

class ChecklistQuestionCreate(BaseModel):
    pergunta: str
    tipo: str

    obrigatoria: bool = True
    exige_evidencia: bool = False


class ChecklistCreate(BaseModel):
    nome: str

    questions: List[ChecklistQuestionCreate]


# =========================
# INSPECTIONS
# =========================

class InspectionAnswerCreate(BaseModel):
    pergunta: str
    resposta: str

    risco: Optional[str] = None

    evidencia: Optional[str] = None


class InspectionCreate(BaseModel):
    client_id: int
    project_id: int
    checklist_id: int

    localizacao: Optional[str] = None

    assinatura: Optional[str] = None

    answers: List[InspectionAnswerCreate]


# =========================
# NON CONFORMITIES
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