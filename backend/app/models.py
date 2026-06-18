from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# =========================
# CLIENTS
# =========================

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=False, nullable=False)

    endereco = Column(String)
    email = Column(String)
    telefone = Column(String)

    cnae = Column(String)
    grau_risco = Column(String)

    numero_funcionarios = Column(Integer)

    projects = relationship(
        "Project",
        back_populates="client"
    )


# =========================
# PROJECTS
# =========================

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    nome = Column(String, nullable=False)
    descricao = Column(Text)

    status = Column(String, default="ativo")

    responsavel = Column(String)

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    client = relationship(
        "Client",
        back_populates="projects"
    )


# =========================
# CHECKLISTS
# =========================

class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True)

    nome = Column(String, nullable=False)

    versao = Column(Integer, default=1)

    bloqueado = Column(Boolean, default=False)

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    questions = relationship(
        "ChecklistQuestion",
        back_populates="checklist"
    )


class ChecklistQuestion(Base):
    __tablename__ = "checklist_questions"

    id = Column(Integer, primary_key=True)

    checklist_id = Column(
        Integer,
        ForeignKey("checklists.id")
    )

    pergunta = Column(Text, nullable=False)

    tipo = Column(String)

    obrigatoria = Column(Boolean, default=True)

    exige_evidencia = Column(
        Boolean,
        default=False
    )

    checklist = relationship(
        "Checklist",
        back_populates="questions"
    )


# =========================
# INSPECTIONS
# =========================

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer)
    project_id = Column(Integer)
    checklist_id = Column(Integer)

    status = Column(String, default="em_andamento")

    localizacao = Column(String)

    assinatura = Column(Text)

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )


class InspectionAnswer(Base):
    __tablename__ = "inspection_answers"

    id = Column(Integer, primary_key=True)

    inspection_id = Column(Integer)

    pergunta = Column(Text)

    resposta = Column(Text)

    risco = Column(String)

    evidencia = Column(Text)


# =========================
# NON CONFORMITIES
# =========================

class NonConformity(Base):
    __tablename__ = "non_conformities"

    id = Column(Integer, primary_key=True)

    inspection_id = Column(Integer)

    origem = Column(String)

    descricao = Column(Text)

    severidade = Column(String)

    status = Column(
        String,
        default="aberta"
    )

    responsavel = Column(String)

    prazo = Column(DateTime)


class NCAction(Base):
    __tablename__ = "nc_actions"

    id = Column(Integer, primary_key=True)

    nc_id = Column(Integer)

    descricao = Column(Text)

    responsavel = Column(String)

    prazo = Column(DateTime)

    status = Column(
        String,
        default="pendente"
    )