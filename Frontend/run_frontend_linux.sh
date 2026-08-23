#!/bin/bash

cd "$(dirname "$0")"
echo -ne "\033]0;OctaFood Frontend\007"

if [ ! -d "node_modules" ]; then
    echo "[1/2] Instalando dependencias - primera vez..."
    npm install
fi

echo "[2/2] Arrancando el frontend en http://localhost:5173 ..."
echo "       Cierra esta ventana o presiona Ctrl+C para detenerlo."
echo ""
npm run dev
