// ─── CLIENTE HTTP DEL BACKEND (FastAPI en :8000) ─────────────────────────────

const API_URL: string =
  (import.meta.env?.VITE_API_URL as string | undefined) ??
  "http://localhost:8000";

const TOKEN_KEY = "octafood_token";

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function setToken(token: string | null): void {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {
    /* almacenamiento no disponible */
  }
}

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

interface ApiOptions {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
  body?: unknown;
  /** Si es true (default) adjunta el Bearer token. */
  auth?: boolean;
}

export async function api<T>(
  path: string,
  options: ApiOptions = {},
): Promise<T> {
  const { method = "GET", body, auth = true } = options;

  const headers: Record<string, string> = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const token = getToken();
  if (auth && token) headers["Authorization"] = `Bearer ${token}`;

  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError(
      0,
      `No se pudo conectar con el backend (${API_URL}). ¿Está corriendo uvicorn?`,
    );
  }

  if (!res.ok) {
    let detail = `Error ${res.status}`;
    try {
      const json = await res.json();
      if (typeof json?.detail === "string") detail = json.detail;
      else if (Array.isArray(json?.detail)) {
        detail = json.detail
          .map((d: { msg?: string }) => d?.msg ?? "")
          .filter(Boolean)
          .join(". ");
      } else if (json?.detail) detail = JSON.stringify(json.detail);
    } catch {
      /* cuerpo no JSON */
    }
    throw new ApiError(res.status, detail);
  }

  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export function apiUrl(): string {
  return API_URL;
}
