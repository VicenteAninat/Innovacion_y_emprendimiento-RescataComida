import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { User } from "../../lib/types";
import {
  getProfileApi,
  loginApi,
  registerApi,
  type RegisterPayload,
} from "../../lib/api/auth";
import { getToken, setToken } from "../../lib/api/client";
import { clearCaches } from "../../lib/data/cache";

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Restaurar sesión si hay un token guardado.
  useEffect(() => {
    let cancelled = false;
    const restore = async () => {
      if (!getToken()) {
        setLoading(false);
        return;
      }
      try {
        const profile = await getProfileApi();
        if (!cancelled) setUser(profile);
      } catch {
        setToken(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    restore();
    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await loginApi(email, password);
    setToken(res.access_token);
    setUser(res.user);
  }, []);

  const register = useCallback(async (payload: RegisterPayload) => {
    await registerApi(payload);
    // Tras registrar, intentamos iniciar sesión directo.
    // Si el proyecto Supabase exige confirmación de correo, login fallará
    // con un mensaje del backend y la UI lo mostrará.
    const res = await loginApi(payload.email, payload.password);
    setToken(res.access_token);
    setUser(res.user);
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    clearCaches();
  }, []);

  const value = useMemo(
    () => ({ user, loading, login, register, logout }),
    [user, loading, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de <AuthProvider>");
  return ctx;
}
