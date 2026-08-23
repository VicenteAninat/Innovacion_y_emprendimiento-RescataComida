# OctaFood - Rescate de alimentos (Innovación y Emprendimiento)

Proyecto de Innova del grupo 4. Desafío de RescataComida.

## Estructura

- `app/` — Backend FastAPI + Supabase (PostgreSQL/PostGIS + Auth)
- `Frontend/` — App móvil React + Vite + Tailwind (ver su README)
- `scripts SQL/` — Esquema de la BD y políticas RLS
- `tests/` — Tests del backend (pytest)
- `seed_demo.py` — Siembra datos de demostración vía la API

## Backend local

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# crear .env con SUPABASE_URL y SUPABASE_KEY (ver .gitignore, no se commitea)
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

> Nota: `gunicorn` de `requirements.txt` no corre en Windows; instálalo aparte
> solo si despliegas en Linux.

## Frontend local

```powershell
cd Frontend
npm install
npm run dev   # http://localhost:5173 (configura VITE_API_URL en Frontend/.env)
```

## Datos de demostración

Con el backend corriendo:

```powershell
.\.venv\Scripts\python.exe seed_demo.py
```

Cuentas: `cliente@octafood.cl` / `comercio@octafood.cl` (`password123`),
`admin_octa@example.com` (`demo1234`).
