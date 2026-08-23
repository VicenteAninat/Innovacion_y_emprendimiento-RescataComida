import { useState, type FormEvent } from "react";
import {
  ArrowLeft,
  Check,
  Lock,
  Mail,
  ShoppingBag,
  Store,
  User,
} from "lucide-react";
import { useAuth } from "./AuthContext";

type Mode = "login" | "register";

export default function LoginScreen({
  defaultMode = "login",
  onBack,
}: {
  defaultMode?: Mode;
  onBack?: () => void;
}) {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<Mode>(defaultMode);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [role, setRole] = useState<"customer" | "worker">("customer");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const switchMode = (m: Mode) => {
    setMode(m);
    setError(null);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (mode === "login" && (!email || !password)) {
      setError("Ingresa tu correo y contraseña.");
      return;
    }
    if (mode === "register" && (!email || password.length < 6)) {
      setError("Ingresa un correo válido y una contraseña de al menos 6 caracteres.");
      return;
    }
    setSubmitting(true);
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register({
          email,
          password,
          name: name || null,
          phone: phone || null,
          role,
          business_id: null,
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado.");
    } finally {
      setSubmitting(false);
    }
  };

  const inputCls =
    "w-full bg-card border border-border rounded-2xl px-4 h-12 text-sm outline-none text-foreground placeholder:text-muted-foreground focus:border-primary transition-colors";

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-1 overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {/* Header */}
        <div className="px-5 pt-6 pb-2">
          <div className="flex items-center gap-3 mb-6">
            {onBack && (
              <button
                onClick={onBack}
                className="w-9 h-9 rounded-full bg-muted flex items-center justify-center"
              >
                <ArrowLeft size={18} className="text-foreground" />
              </button>
            )}
            <div>
              <h1
                className="font-black text-2xl text-foreground"
                style={{ fontFamily: "'Righteous', sans-serif" }}
              >
                OctaFood
              </h1>
              <p className="text-xs text-muted-foreground">
                Rescata comida, no la desperdicies.
              </p>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex bg-muted rounded-2xl p-1 mb-6">
            <button
              onClick={() => switchMode("login")}
              className={`flex-1 h-11 rounded-xl text-sm font-bold transition-all ${
                mode === "login"
                  ? "bg-card shadow-sm text-foreground"
                  : "text-muted-foreground"
              }`}
            >
              Iniciar sesión
            </button>
            <button
              onClick={() => switchMode("register")}
              className={`flex-1 h-11 rounded-xl text-sm font-bold transition-all ${
                mode === "register"
                  ? "bg-card shadow-sm text-foreground"
                  : "text-muted-foreground"
              }`}
            >
              Registrarme
            </button>
          </div>

          {error && (
            <div className="mb-4 bg-primary/10 border border-primary/20 rounded-2xl p-3.5">
              <p className="text-xs text-foreground leading-relaxed">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3">
            {mode === "register" && (
              <>
                <div className="flex items-center gap-2 bg-card border border-border rounded-2xl px-4 h-12">
                  <User size={16} className="text-muted-foreground shrink-0" />
                  <input
                    type="text"
                    placeholder="Nombre (opcional)"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="flex-1 bg-transparent text-sm outline-none text-foreground placeholder:text-muted-foreground"
                  />
                </div>
                <div className="flex items-center gap-2 bg-card border border-border rounded-2xl px-4 h-12">
                  <Store size={16} className="text-muted-foreground shrink-0" />
                  <input
                    type="text"
                    placeholder="Teléfono (opcional)"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="flex-1 bg-transparent text-sm outline-none text-foreground placeholder:text-muted-foreground"
                  />
                </div>
              </>
            )}

            <div className="flex items-center gap-2 bg-card border border-border rounded-2xl px-4 h-12">
              <Mail size={16} className="text-muted-foreground shrink-0" />
              <input
                type="email"
                placeholder="Correo electrónico"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="flex-1 bg-transparent text-sm outline-none text-foreground placeholder:text-muted-foreground"
              />
            </div>

            <div className="flex items-center gap-2 bg-card border border-border rounded-2xl px-4 h-12">
              <Lock size={16} className="text-muted-foreground shrink-0" />
              <input
                type="password"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="flex-1 bg-transparent text-sm outline-none text-foreground placeholder:text-muted-foreground"
              />
            </div>

            {mode === "register" && (
              <div>
                <p className="text-xs font-bold text-muted-foreground mb-2">
                  ¿Qué tipo de cuenta necesitas?
                </p>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setRole("customer")}
                    className={`rounded-2xl border-2 p-3 text-left transition-all ${
                      role === "customer"
                        ? "border-primary bg-primary/10"
                        : "border-border bg-card"
                    }`}
                  >
                    <ShoppingBag size={20} className="mb-1 text-foreground" />
                    <span className="text-xs font-bold text-foreground block">
                      Soy cliente
                    </span>
                    <p className="text-[9px] text-muted-foreground">
                      Quiero rescatar bolsas
                    </p>
                  </button>
                  <button
                    type="button"
                    onClick={() => setRole("worker")}
                    className={`rounded-2xl border-2 p-3 text-left transition-all ${
                      role === "worker"
                        ? "border-primary bg-primary/10"
                        : "border-border bg-card"
                    }`}
                  >
                    <Store size={20} className="mb-1 text-foreground" />
                    <span className="text-xs font-bold text-foreground block">
                      Soy comercio
                    </span>
                    <p className="text-[9px] text-muted-foreground">
                      Quiero publicar excedentes
                    </p>
                  </button>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full h-14 rounded-2xl bg-primary text-white font-bold text-base active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-60"
            >
              {submitting ? (
                <>
                  <div className="w-4 h-4 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                  Procesando...
                </>
              ) : (
                <>
                  <Check size={18} />
                  {mode === "login" ? "Entrar" : "Crear cuenta"}
                </>
              )}
            </button>
          </form>

          <p className="text-[10px] text-muted-foreground text-center mt-5 leading-relaxed">
            Las cuentas se gestionan con Supabase Auth. Si tu cuenta de
            comercio aún no está vinculada a un local, pide a un administrador
            que la asocie.
          </p>
        </div>
      </div>
    </div>
  );
}
