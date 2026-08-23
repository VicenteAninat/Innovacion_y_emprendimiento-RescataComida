@echo off
cd /d "%~dp0"
title OctaFood Backend

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creando entorno virtual...
    python -m venv .venv 2>nul
    if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
    if not exist ".venv\Scripts\python.exe" (
        echo.
        echo ERROR: No se encontro Python instalado.
        echo Instalalo desde https://www.python.org/downloads/ y vuelve a ejecutar este archivo.
        pause
        exit /b 1
    )
)

.venv\Scripts\python.exe -c "import fastapi, supabase" 2>nul
if errorlevel 1 (
    echo [2/3] Instalando dependencias - primera vez...
    .venv\Scripts\python.exe -m pip install -r requirements-win.txt
)

if not exist ".env" (
    echo.
    echo ERROR: Falta el archivo .env en la raiz del proyecto.
    echo Copia .env.example a .env y completa SUPABASE_URL y SUPABASE_KEY.
    pause
    exit /b 1
)

echo [3/3] Arrancando el backend en http://localhost:8000 ...
echo        Docs interactivos: http://localhost:8000/docs
echo        Cierra esta ventana o presiona Ctrl+C para detenerlo.
echo.
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
