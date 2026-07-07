"""Supabase client configuration and initialization module."""

import os
from supabase import create_client, Client

def load_env_file():
    """Loads environment variables from a .env file located at the project root.

    This function searches for a .env file in the project's root directory,
    parses its contents, and updates the environment variables (os.environ)
    for keys that are not already defined.

    Raises:
        OSError: If there is an issue reading the .env file.
    """
    # Encontrar el archivo .env en la raíz del proyecto
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

# Cargar .env si existe
load_env_file()

supabase_url = os.environ.get("SUPABASE_URL", "")
# Corregir el prefijo del URL en caso de que venga como 'ttps://'
if supabase_url.startswith("ttps://"):
    supabase_url = "https://" + supabase_url[7:]

supabase_key = os.environ.get("SUPABASE_KEY", "")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured in environment variables or .env")

# Inicializar cliente singleton
supabase: Client = create_client(supabase_url, supabase_key)
