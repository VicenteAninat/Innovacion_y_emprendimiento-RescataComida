#!/bin/bash

cd "$(dirname "$0")"
echo -ne "\033]0;OctaFood Backend\007"

if [ ! -f ".venv/bin/python" ]; then
    echo "[1/3] Creando entorno virtual..."
    python3 -m venv .venv 2>/dev/null
    if [ ! -f ".venv/bin/python" ]; then
        echo ""
        echo "ERROR: No se encontró Python 3 instalado o el paquete python3-venv."
        echo "Asegúrate de tenerlos instalados y vuelve a ejecutar este archivo."
        exit 1
    fi
fi

.venv/bin/python -c "import fastapi, supabase" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[2/3] Instalando dependencias - primera vez..."
    .venv/bin/python -m pip install -r requirements.txt
fi

if [ ! -f ".env" ]; then
    echo ""
    echo "ERROR: Falta el archivo .env en la raíz del proyecto."
    echo "Copia .env.example a .env y completa SUPABASE_URL y SUPABASE_KEY."
    exit 1
fi

echo "[3/3] Arrancando el backend en http://localhost:8081 ..."
echo "       Docs interactivos: http://localhost:8081/docs"
echo "       Cierra esta ventana o presiona Ctrl+C para detenerlo."
echo ""
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8081
