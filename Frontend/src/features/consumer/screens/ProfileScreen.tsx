import {
  Bell,
  ChevronRight,
  Coins,
  CreditCard,
  FileText,
  Gift,
  Leaf,
  LogOut,
  MapPin,
  ShoppingBag,
  Star,
  Store,
} from "lucide-react";
import type { User } from "../../../lib/types";
import SectionHeader from "../../shared/SectionHeader";

export default function ProfileScreen({
  user,
  onOpenMerchant,
  onLogout,
}: {
  user: User;
  onOpenMerchant: () => void;
  onLogout: () => void;
}) {
  const initials = (user.name || user.email || "U").slice(0, 1).toUpperCase();
  const isMerchant = user.role === "worker" || user.role === "admin";

  return (
    <div className="pb-6">
      <div className="px-5 pt-5 pb-4">
        <h1
          className="font-black text-2xl text-foreground"
          style={{ fontFamily: "'Righteous', sans-serif" }}
        >
          Mi Perfil
        </h1>
      </div>

      <div
        className="mx-5 mb-5 rounded-3xl p-5 relative overflow-hidden"
        style={{ background: "#1C0800" }}
      >
        <div className="absolute top-0 right-0 w-36 h-36 rounded-full bg-white/5 pointer-events-none" />
        <div className="absolute -bottom-6 left-6 w-20 h-20 bg-secondary/15 rotate-45 pointer-events-none" />
        <div className="absolute top-8 right-12 w-4 h-4 rounded-full bg-primary/40 pointer-events-none" />
        <div className="flex items-center gap-4 relative z-10">
          <div className="w-16 h-16 rounded-2xl bg-primary flex items-center justify-center text-white text-3xl font-black shrink-0">
            {initials}
          </div>
          <div className="min-w-0">
            <p className="text-white font-bold text-lg truncate">
              {user.name || "Rescatador"}
            </p>
            <p className="text-white/50 text-sm truncate">{user.email}</p>
            <div className="flex items-center gap-1 mt-1">
              <Star size={11} fill="#FFD600" className="text-secondary" />
              <span className="text-secondary text-xs font-bold">
                {isMerchant ? "Cuenta de comercio" : "Héroe del Rescate"}
              </span>
            </div>
          </div>
        </div>
      </div>

      <SectionHeader title="Mi Impacto Total" />
      <div className="grid grid-cols-3 gap-3 px-5 mb-5">
        {[
          { icon: ShoppingBag, value: "—", label: "Bolsas rescatadas" },
          { icon: Coins, value: "—", label: "Ahorrado" },
          { icon: Leaf, value: "—", label: "CO₂ evitado" },
        ].map((s) => {
          const Icon = s.icon;
          return (
            <div
              key={s.label}
              className="bg-card rounded-2xl p-3 border border-border text-center"
            >
              <Icon size={20} className="mx-auto mb-1 text-foreground" />
              <p className="font-black text-sm text-foreground">{s.value}</p>
              <p className="text-[9px] text-muted-foreground leading-tight mt-0.5">
                {s.label}
              </p>
            </div>
          );
        })}
      </div>

      {/* Merchant CTA */}
      <div className="px-5 mb-5">
        <button
          onClick={onOpenMerchant}
          className="w-full bg-secondary rounded-2xl p-4 flex items-center gap-3 border-2 border-foreground/10 active:scale-[0.98] transition-transform"
        >
          <div className="w-10 h-10 rounded-xl bg-foreground flex items-center justify-center shrink-0">
            <Store size={18} className="text-background" />
          </div>
          <div className="flex-1 text-left">
            <p className="font-black text-sm text-foreground">
              {isMerchant ? "Abrir panel de comercio" : "Cambiar a modo proveedor"}
            </p>
            <p className="text-[10px] text-foreground/60">
              Gestiona tu comercio y publica bolsas
            </p>
          </div>
          <ChevronRight size={16} className="text-foreground/50" />
        </button>
      </div>

      <SectionHeader title="Configuración" />
      <div className="px-5 flex flex-col gap-2">
        {[
          { icon: Bell, label: "Notificaciones", desc: "Alertas de nuevas bolsas" },
          { icon: MapPin, label: "Ubicaciones", desc: "Casa, Trabajo..." },
          { icon: CreditCard, label: "Métodos de pago", desc: "Mastercard ···· 4467" },
          { icon: Gift, label: "Código de referido", desc: "Invita y gana créditos" },
          { icon: FileText, label: "Certificado tributario", desc: "Donaciones deducibles 2025" },
        ].map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.label}
              className="bg-card rounded-2xl flex items-center gap-3 p-3.5 border border-border w-full text-left"
            >
              <Icon size={18} className="text-muted-foreground shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-foreground">
                  {item.label}
                </p>
                <p className="text-[10px] text-muted-foreground">{item.desc}</p>
              </div>
              <ChevronRight
                size={16}
                className="text-muted-foreground shrink-0"
              />
            </button>
          );
        })}
        <button
          onClick={onLogout}
          className="bg-card rounded-2xl flex items-center gap-3 p-3.5 border border-border w-full text-left"
        >
          <LogOut size={18} className="text-muted-foreground shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-foreground">
              Cerrar sesión
            </p>
            <p className="text-[10px] text-muted-foreground">
              Cambia de cuenta o sal de la app
            </p>
          </div>
          <ChevronRight size={16} className="text-muted-foreground shrink-0" />
        </button>
      </div>
    </div>
  );
}
