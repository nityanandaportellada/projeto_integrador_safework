@echo off

echo Iniciando backend...
cd backend

start powershell -NoExit -ExecutionPolicy Bypass -Command "if (!(Test-Path venv)) { python -m venv venv }; venv\Scripts\python -m pip install --upgrade pip; venv\Scripts\python -m pip install -r requirements.txt; venv\Scripts\python -m uvicorn app.main:app --reload"

cd ..

echo Iniciando frontend...
cd frontend

start powershell -NoExit -ExecutionPolicy Bypass -Command "python -m http.server 5500"