import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  BarChart3,
  Bell,
  ChevronRight,
  CreditCard,
  FileText,
  LogOut,
  MapPin,
  Pencil,
  Star,
  User,
} from "lucide-react";
import type { Business } from "../../lib/types";
import { categoryIcon } from "../../lib/images";
import {
  cachedRating,
  getBusinessReviewsCached,
} from "../../lib/data/cache";
import SectionHeader from "../shared/SectionHeader";

export default function ProviderStoreScreen({
  business,
  onSwitchToConsumer,
  onLogout,
}: {
  business: Business;
  onSwitchToConsumer: () => void;
  onLogout: () => void;
}) {
  const [ratingInfo, setRatingInfo] = useState<{
    rating: number;
    count: number;
  } | null>(null);

  useEffect(() => {
    let cancelled = false;
    getBusinessReviewsCached(business.id ?? 0).then(() => {
      if (!cancelled) setRatingInfo(cachedRating(business.id ?? 0));
    });
    return () => {
      cancelled = true;
    };
  }, [business.id]);

  const StoreIcon = useMemo(
    () => categoryIcon(business.category),
    [business.category],
  );

  return (
    <div className="pb-6">
      <div className="px-5 pt-5 pb-4">
        <h1
          className="font-black text-2xl text-foreground"
          style={{ fontFamily: "'Righteous', sans-serif" }}
        >
          Mi Comercio
        </h1>
      </div>

      {/* Store card */}
      <div
        className="mx-5 mb-5 rounded-3xl p-5 relative overflow-hidden"
        style={{ background: "#1C0800" }}
      >
        <div className="absolute top-0 right-0 w-36 h-36 rounded-full bg-white/5 pointer-events-none" />
        <div className="absolute -bottom-6 left-6 w-20 h-20 bg-primary/20 rotate-45 pointer-events-none" />
        <div className="relative z-10 flex items-center gap-4 mb-4">
          <div className="w-16 h-16 rounded-2xl bg-primary/30 flex items-center justify-center shrink-0">
            <StoreIcon size={26} className="text-white" />
          </div>
          <div className="min-w-0">
            <p className="text-white font-bold text-lg truncate">
              {business.name || "Sin nombre"}
            </p>
            <p className="text-white/50 text-sm truncate">
              {business.address || "Dirección no registrada"}
            </p>
            <div className="flex items-center gap-1 mt-1">
              {ratingInfo ? (
                <>
                  <Star size={11} fill="#FFD600" className="text-secondary" />
                  <span className="text-secondary text-xs font-bold">
                    {ratingInfo.rating}
                  </span>
                  <span className="text-white/40 text-xs ml-1">
                    · {ratingInfo.count} reseñas
                  </span>
                </>
              ) : (
                <span className="text-white/40 text-xs">Sin reseñas aún</span>
              )}
            </div>
          </div>
        </div>
        <button className="relative z-10 w-full h-9 rounded-xl border border-white/20 text-white/70 text-xs font-bold flex items-center justify-center gap-2">
          <Pencil size={12} />
          Editar información del comercio
        </button>
      </div>

      {/* Settings */}
      <SectionHeader title="Configuración" />
      <div className="px-5 flex flex-col gap-2 mb-5">
        {[
          { icon: Bell, label: "Notificaciones de pedidos", desc: "Alertas en tiempo real" },
          { icon: MapPin, label: "Dirección del local", desc: business.address ?? "Sin dirección registrada" },
          { icon: CreditCard, label: "Datos bancarios", desc: "Cuenta para transferencias" },
          { icon: FileText, label: "Certificados de donación", desc: "Documentos tributarios 2025" },
          { icon: BarChart3, label: "Estadísticas completas", desc: "Historial de ventas e impacto" },
        ].map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.label}
              className="bg-card rounded-2xl flex items-center gap-3 p-3.5 border border-border w-full text-left"
            >
              <Icon size={18} className="text-muted-foreground shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-bold text-foreground">{item.label}</p>
                <p className="text-[10px] text-muted-foreground truncate">
                  {item.desc}
                </p>
              </div>
              <ChevronRight size={14} className="text-muted-foreground shrink-0" />
            </button>
          );
        })}
      </div>

      {/* Switch to consumer */}
      <div className="px-5 flex flex-col gap-2">
        <button
          onClick={onSwitchToConsumer}
          className="w-full bg-muted rounded-2xl p-4 flex items-center gap-3 border border-border active:scale-[0.98] transition-transform"
        >
          <div className="w-10 h-10 rounded-xl bg-card border border-border flex items-center justify-center shrink-0">
            <User size={18} className="text-foreground" />
          </div>
          <div className="flex-1 text-left">
            <p className="font-black text-sm text-foreground">
              Cambiar a modo consumidor
            </p>
            <p className="text-[10px] text-muted-foreground">
              Explora bolsas como cliente
            </p>
          </div>
          <ArrowRight size={16} className="text-muted-foreground" />
        </button>

        <button
          onClick={onLogout}
          className="w-full bg-card rounded-2xl p-4 flex items-center gap-3 border border-border active:scale-[0.98] transition-transform"
        >
          <div className="w-10 h-10 rounded-xl bg-muted flex items-center justify-center shrink-0">
            <LogOut size={18} className="text-foreground" />
          </div>
          <div className="flex-1 text-left">
            <p className="font-black text-sm text-foreground">Cerrar sesión</p>
            <p className="text-[10px] text-muted-foreground">
              Salir de la cuenta de comercio
            </p>
          </div>
          <ArrowRight size={16} className="text-muted-foreground" />
        </button>
      </div>
    </div>
  );
}
