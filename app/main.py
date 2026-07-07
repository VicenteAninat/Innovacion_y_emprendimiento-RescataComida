"""Main Application Entrypoint.

This module initializes the FastAPI application, configures CORS middleware,
registers all API routes, and starts the server using uvicorn when run directly.
"""

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.controller import api_router

app = FastAPI(
    title="OCTAFOOD API",
    description="API para la gestión de rescate de alimentos (Innovación y Emprendimiento)",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router maestro (universal router)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
