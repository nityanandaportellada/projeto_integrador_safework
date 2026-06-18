from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base

from app.routers import clients
from app.routers import projects
from app.routers import checklists
from app.routers import inspections
from app.routers import non_conformities
from app.routers import reports
from app.routers import dashboard


# Cria tabelas SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SafeWork API",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas
app.include_router(clients.router)
app.include_router(projects.router)
app.include_router(checklists.router)
app.include_router(inspections.router)
app.include_router(non_conformities.router)
app.include_router(reports.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "message": "SafeWork API Online"
    }
