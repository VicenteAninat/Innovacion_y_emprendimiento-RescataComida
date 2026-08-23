@echo off
cd /d "%~dp0"
title OctaFood Frontend

if not exist "node_modules" (
    echo [1/2] Instalando dependencias - primera vez...
    call npm install
)

echo [2/2] Arrancando el frontend en http://localhost:5173 ...
echo        Cierra esta ventana o presiona Ctrl+C para detenerlo.
echo.
call npm run dev

pause
