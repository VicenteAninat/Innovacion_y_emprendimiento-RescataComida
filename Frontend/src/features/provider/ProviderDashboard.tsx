import { useMemo } from "react";
import {
  CalendarDays,
  Clock,
  Leaf,
  Plus,
  ShoppingBag,
  Star,
} from "lucide-react";
import type { Business, Offer, Reservation } from "../../lib/types";
import { fmt } from "../../lib/format";
import { categoryIcon } from "../../lib/images";
import { clientAlias } from "../../lib/data/mappers";
import SectionHeader from "../shared/SectionHeader";

const STATUS_MAP: Record<
  string,
  { label: string; color: string; bg: string }
> = {
  paid: { label: "Pagado", color: "text-[#00C87A]", bg: "bg-[#00C87A]/10" },
  pending: { label: "Pendiente", color: "text-secondary", bg: "bg-secondary/10" },
  collected: { label: "Retirado", color: "text-muted-foreground", bg: "bg-muted" },
  completed: { label: "Completado", color: "text-[#00C87A]", bg: "bg-[#00C87A]/10" },
  cancelled: { label: "Cancelado", color: "text-muted-foreground", bg: "bg-muted" },
};

function isToday(iso: string | null | undefined): boolean {
  if (!iso) return false;
  const d = new Date(iso);
  const now = new Date();
  return (
    d.getFullYear() === now.getFullYear() &&
    d.getMonth() === now.getMonth() &&
    d.getDate() === now.getDate()
  );
}

export default function ProviderDashboard({
  business,
  offers,
  reservations,
  onPublish,
}: {
  business: Business;
  offers: Offer[];
  reservations: Reservation[];
  onPublish: () => void;
}) {
  const stats = useMemo(() => {
    const todayReservations = reservations.filter((r) =>
      isToday(r.created_at),
    );
    const todayRevenue = todayReservations
      .filter((r) => r.status === "paid" || r.status === "collected")
      .reduce((s, r) => s + (r.total_price ?? 0), 0);
    const bagsLeft = offers
      .filter((o) => o.status === "active")
      .reduce((s, o) => s + (o.quantity_available ?? 0), 0);
    const offerById = new Map(offers.map((o) => [o.id ?? 0, o]));
    const collected = reservations.filter((r) => r.status === "collected");
    const totalRescued = collected.reduce((s, r) => s + r.quantity, 0);
    const co2Total = collected.reduce((s, r) => {
      const offer = offerById.get(r.offer_id);
      return s + (offer?.co2_avoided_per_unit ?? 0) * r.quantity;
    }, 0);
    const memberSince = business.created_at
      ? new Date(business.created_at).toLocaleDateString("es-CL", {
          month: "long",
          year: "numeric",
        })
      : "—";
    return { todayReservations, todayRevenue, bagsLeft, totalRescued, co2Total, memberSince };
  }, [business, offers, reservations]);

  const recentOrders = useMemo(
    () =>
      [...reservations]
        .sort((a, b) =>
          (b.created_at ?? "").localeCompare(a.created_at ?? ""),
        )
        .slice(0, 3),
    [reservations],
  );

  const offerById = useMemo(
    () => new Map(offers.map((o) => [o.id ?? 0, o])),
    [offers],
  );

  const CategoryIcon = categoryIcon(business.category);

  return (
    <div className="pb-6">
      {/* Header */}
      <div
        className="px-5 pt-5 pb-6 relative overflow-hidden"
        style={{ background: "#1C0800" }}
      >
        <div className="absolute top-0 right-0 w-40 h-40 rounded-full bg-white/5 pointer-events-none" />
        <div className="absolute -bottom-8 left-4 w-24 h-24 bg-primary/20 rotate-12 pointer-events-none" />
        <div className="relative z-10">
          <p className="text-white/50 text-xs font-semibold uppercase tracking-widest mb-1">
            Panel de comercio
          </p>
          <h1
            className="font-black text-2xl text-white mb-1"
            style={{ fontFamily: "'Righteous', sans-serif" }}
          >
            {business.name || `Comercio #${business.id ?? ""}`}
          </h1>
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1">
              <Star size={11} fill="#FFD600" className="text-secondary" />
              <span className="text-secondary text-xs font-bold">
                {business.is_premium ? "Premium" : "Activo"}
              </span>
            </div>
            <span className="text-white/30 text-xs">·</span>
            <span className="text-white/50 text-xs">
              {business.address || "Dirección no registrada"}
            </span>
          </div>
        </div>
      </div>

      {/* Today's stats */}
      <div className="px-5 -mt-3 mb-5">
        <div className="bg-card border border-border rounded-3xl p-4 shadow-sm">
          <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-3">
            Hoy
          </p>
          <div className="grid grid-cols-3 gap-3 text-center">
            {[
              {
                label: "Pedidos",
                value: String(stats.todayReservations.length),
                color: "text-primary",
              },
              {
                label: "Ingresos",
                value: fmt(stats.todayRevenue),
                color: "text-accent",
              },
              {
                label: "Bolsas left",
                value: String(stats.bagsLeft),
                color: "text-secondary",
              },
            ].map((s) => (
              <div key={s.label}>
                <p className={`font-black text-lg ${s.color}`}>{s.value}</p>
                <p className="text-[9px] text-muted-foreground leading-tight">
                  {s.label}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick publish CTA */}
      <div className="px-5 mb-5">
        <button
          onClick={onPublish}
          className="w-full h-14 rounded-2xl bg-primary text-white font-bold flex items-center justify-center gap-2 active:scale-[0.98] transition-transform"
          style={{ fontFamily: "'Righteous', sans-serif" }}
        >
          <Plus size={20} />
          Publicar nueva bolsa
        </button>
      </div>

      {/* Incoming orders preview */}
      <SectionHeader title="Pedidos recientes" />
      <div className="px-5 flex flex-col gap-3 mb-5">
        {recentOrders.map((order) => {
          const s = STATUS_MAP[order.status] ?? STATUS_MAP.pending;
          const offer = offerById.get(order.offer_id);
          return (
            <div
              key={order.id}
              className="bg-card border border-border rounded-2xl p-3 flex items-center gap-3"
            >
              <div className="w-10 h-10 rounded-xl bg-muted flex items-center justify-center shrink-0">
                <CategoryIcon size={18} className="text-foreground" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-bold text-sm text-foreground truncate">
                  {clientAlias(order.user_id)} — {offer?.title ?? "Bolsa"}
                </p>
                <div className="flex items-center gap-2 mt-0.5">
                  <Clock size={10} className="text-muted-foreground" />
                  <span className="text-[10px] text-muted-foreground">
                    x{order.quantity} unidades
                  </span>
                </div>
              </div>
              <div className="shrink-0 text-right">
                <p className="font-black text-sm text-foreground">
                  {fmt(order.total_price ?? 0)}
                </p>
                <span
                  className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full ${s.bg} ${s.color}`}
                >
                  {s.label}
                </span>
              </div>
            </div>
          );
        })}
        {recentOrders.length === 0 && (
          <p className="text-xs text-muted-foreground text-center py-4">
            Aún no hay pedidos registrados.
          </p>
        )}
      </div>

      {/* Lifetime impact */}
      <SectionHeader title="Impacto acumulado" />
      <div className="px-5">
        <div className="bg-accent/10 border border-accent/20 rounded-2xl p-4">
          <div className="grid grid-cols-3 gap-3 text-center">
            {[
              {
                icon: ShoppingBag,
                value: String(stats.totalRescued),
                label: "Bolsas rescatadas",
              },
              {
                icon: Leaf,
                value: `${stats.co2Total.toFixed(1)} kg`,
                label: "CO₂ evitado",
              },
              {
                icon: CalendarDays,
                value: stats.memberSince,
                label: "Miembro desde",
              },
            ].map((s) => {
              const Icon = s.icon;
              return (
                <div key={s.label}>
                  <Icon size={22} className="mx-auto mb-1 text-foreground" />
                  <p className="font-black text-xs text-foreground">{s.value}</p>
                  <p className="text-[9px] text-muted-foreground leading-tight mt-0.5">
                    {s.label}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
