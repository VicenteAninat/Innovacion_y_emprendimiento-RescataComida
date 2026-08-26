import { useCallback, useEffect, useState } from "react";
import { Check, Clock, Edit, Leaf, MapPin, Zap } from "lucide-react";
import type { Order } from "../../../lib/types";
import { fmt } from "../../../lib/format";
import { getMyReservationsApi, payReservationApi, cancelReservationApi } from "../../../lib/api/reservations";
import { reservationToOrder } from "../../../lib/data/mappers";
import {
  getBusinessReviewsCached,
  reservationHasReview,
} from "../../../lib/data/cache";
import SectionHeader from "../../shared/SectionHeader";

const STATUS_LABELS: Record<string, string> = {
  pending: "Pendiente de pago",
  paid: "Pagado",
  collected: "Retirado",
  completed: "Completado",
  cancelled: "Cancelado",
};

export default function OrdersScreen({
  onOpenReview,
  onRepeat,
  refreshToken,
}: {
  onOpenReview: (order: Order) => void;
  onRepeat: (offerId: number) => void;
  refreshToken: number;
}) {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [reviewedIds, setReviewedIds] = useState<Set<number>>(new Set());

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const reservations = await getMyReservationsApi();
      const mapped = await Promise.all(
        reservations.map((r) => reservationToOrder(r)),
      );
      mapped.sort(
        (a, b) =>
          (a.active ? 1 : 0) - (b.active ? 1 : 0) ||
          b.id - a.id,
      );
      setOrders(mapped);

      // Determinar qué pedidos ya tienen reseña
      const reviewed = new Set<number>();
      const filtered = mapped.filter((o) => !o.active && o.restaurantId > 0);
      for (const o of filtered) {
        try {
          await getBusinessReviewsCached(o.restaurantId);
          if (reservationHasReview(o.restaurantId, o.id)) {
            reviewed.add(o.id);
          }
        } catch { /* ignorar */ }
      }
      setReviewedIds(reviewed);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar pedidos.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load, refreshToken]);

  const active = orders.filter((o) => o.active);
  const past = orders.filter((o) => !o.active);
  const totalDonated = orders.reduce((sum, o) => sum + o.donated, 0);

  // Métricas de impacto
  const rescuedBags = past
    .filter((o) => o.status === "collected" || o.status === "completed")
    .reduce((sum, o) => sum + o.quantity, 0);
  const moneySaved = past.reduce(
    (sum, o) => sum + Math.max(0, o.originalValue - o.price) * o.quantity,
    0,
  );
  const co2Avoided = past.reduce((sum, o) => sum + o.co2Saved, 0);

  const runAction = async (fn: () => Promise<unknown>) => {
    setActionError(null);
    try {
      await fn();
      await load();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Error en la acción.");
    }
  };

  return (
    <div className="pb-6">
      <div className="px-5 pt-5 pb-4">
        <h1
          className="font-black text-2xl text-foreground"
          style={{ fontFamily: "'Righteous', sans-serif" }}
        >
          Mis Pedidos
        </h1>
      </div>

      {actionError && (
        <div className="mx-5 mb-4 bg-primary/10 border border-primary/20 rounded-2xl p-3.5">
          <p className="text-xs text-foreground leading-relaxed">{actionError}</p>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center py-14">
          <div className="w-8 h-8 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
        </div>
      )}

      {!loading && error && (
        <div className="mx-5 bg-primary/10 border border-primary/20 rounded-2xl p-4">
          <p className="text-xs text-foreground leading-relaxed">{error}</p>
          <button
            onClick={load}
            className="mt-3 h-9 px-4 rounded-xl bg-primary text-white text-xs font-bold"
          >
            Reintentar
          </button>
        </div>
      )}

      {!loading && !error && active.length > 0 && (
        <>
          <SectionHeader title="En curso" />
          <div className="px-5 mb-5 flex flex-col gap-4">
            {active.map((order) => (
              <div
                key={order.id}
                className="rounded-3xl p-4 relative overflow-hidden"
                style={{ background: "#FF4422" }}
              >
                <div className="absolute top-2 right-8 w-20 h-20 rounded-full bg-white/10 pointer-events-none" />
                <div className="absolute -bottom-4 right-4 w-12 h-12 rounded-full bg-white/10 pointer-events-none" />
                {/* Header row */}
                <div className="flex items-center gap-3 relative z-10 mb-4">
                  <div className="w-12 h-12 rounded-2xl overflow-hidden bg-white/20 shrink-0">
                    <img
                      src={order.image}
                      alt={order.restaurant}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-bold text-sm truncate">
                      {order.restaurant}
                    </p>
                    <p className="text-white/50 text-[11px]">{order.code}</p>
                  </div>
                  <div className="flex items-center gap-1.5 bg-black/20 rounded-full px-2.5 py-1 shrink-0">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#FFD600] animate-pulse" />
                    <span className="text-white text-[11px] font-bold">
                      {STATUS_LABELS[order.status] ?? order.status}
                    </span>
                  </div>
                </div>

                {/* Pickup time — hero element */}
                <div className="relative z-10 bg-white/15 rounded-2xl px-4 py-3 mb-3 border border-white/20">
                  <p className="text-white/60 text-[10px] font-semibold uppercase tracking-widest mb-1">
                    Retira hoy entre
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Clock size={22} className="text-[#FFD600]" />
                      <span
                        className="text-white font-black text-2xl leading-none"
                        style={{ fontFamily: "'Righteous', sans-serif" }}
                      >
                        {order.pickup}
                      </span>
                    </div>
                    <span className="text-white font-black text-base">
                      {fmt(order.price)}
                    </span>
                  </div>
                </div>

                {/* Address */}
                <div className="relative z-10 flex items-center gap-2 text-white/60 text-xs">
                  <MapPin size={12} />
                  <span>{order.restaurant}</span>
                </div>

                {/* Acciones */}
                <div className="relative z-10 flex gap-2 mt-4">
                  {order.status === "pending" && (
                    <button
                      onClick={() => runAction(() => payReservationApi(order.id))}
                      className="flex-1 h-10 rounded-xl bg-[#FFD600] text-foreground text-xs font-black flex items-center justify-center gap-1"
                    >
                      <Zap size={13} />
                      Pagar ahora
                    </button>
                  )}
                  <button
                    onClick={() => runAction(() => cancelReservationApi(order.id))}
                    className="flex-1 h-10 rounded-xl bg-white/15 border border-white/25 text-white text-xs font-bold flex items-center justify-center gap-1"
                  >
                    <Edit size={12} />
                    Cancelar reserva
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {!loading && !error && (
        <SectionHeader title="Historial" />
      )}
      <div className="px-5 flex flex-col gap-3 mb-5">
        {!loading &&
          !error &&
          past.map((order) => {
            const hasReview = reviewedIds.has(order.id);
            const reviewable =
              order.status === "collected" || order.status === "completed";
            return (
              <div
                key={order.id}
                className="bg-card rounded-2xl p-3 border border-border"
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-12 h-12 rounded-xl overflow-hidden bg-muted shrink-0">
                    <img
                      src={order.image}
                      alt={order.restaurant}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-sm text-foreground truncate">
                      {order.restaurant}
                    </p>
                    <p className="text-[10px] text-muted-foreground">
                      {order.date}
                    </p>
                    <div className="flex items-center gap-3 mt-0.5">
                      <div className="flex items-center gap-1">
                        <Check size={10} className="text-accent" />
                        <span className="text-[10px] text-muted-foreground">
                          {STATUS_LABELS[order.status] ?? order.status}
                        </span>
                      </div>
                      {order.donated > 0 && (
                        <div className="flex items-center gap-1">
                          <Leaf size={9} className="text-accent" />
                          <span className="text-[10px] text-accent font-semibold">
                            {fmt(order.donated)} donado
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="font-black text-sm text-foreground">
                      {fmt(order.price)}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => onRepeat(order.offerId)}
                    className="flex-1 h-9 rounded-xl bg-muted text-foreground text-xs font-bold flex items-center justify-center gap-1"
                  >
                    Repetir
                  </button>
                  {reviewable && hasReview ? (
                    <button
                      disabled
                      className="flex-1 h-9 rounded-xl bg-accent/10 text-accent text-xs font-bold flex items-center justify-center gap-1"
                    >
                      <Check size={13} />
                      Reseña publicada
                    </button>
                  ) : reviewable ? (
                    <button
                      onClick={() => onOpenReview(order)}
                      className="flex-1 h-9 rounded-xl bg-primary text-white text-xs font-bold flex items-center justify-center gap-1"
                    >
                      <Edit size={13} />
                      Escribir reseña
                    </button>
                  ) : (
                    <div className="flex-1" />
                  )}
                </div>
              </div>
            );
          })}
      </div>

      {/* Food bank donations */}
      {!loading && !error && totalDonated > 0 && (
        <div className="mx-5 mb-4 bg-accent/10 border border-accent/20 rounded-2xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <Leaf size={14} className="text-accent" />
            <p className="font-bold text-sm text-foreground">
              Donaciones a Banco de Alimentos
            </p>
          </div>
          <p className="text-xs text-muted-foreground mb-2">
            Has donado{" "}
            <span className="font-black text-accent">{fmt(totalDonated)}</span>{" "}
            a familias vulnerables. Deducible de impuestos (Ley 20.241).
          </p>
          <button className="text-xs text-accent font-bold">
            Descargar certificado →
          </button>
        </div>
      )}

      {/* Impact this month */}
      {!loading && !error && (
        <div className="mx-5 bg-muted rounded-2xl p-4 border border-border">
          <div className="flex items-center gap-2 mb-3">
            <Zap size={14} className="text-primary" />
            <p className="font-bold text-sm text-foreground">
              Tu impacto total
            </p>
          </div>
          <div className="grid grid-cols-3 gap-2 text-center">
            {[
              { label: "Bolsas rescatadas", value: String(rescuedBags) },
              { label: "Dinero ahorrado", value: fmt(moneySaved) },
              {
                label: "CO₂ evitado",
                value: `${co2Avoided.toFixed(1)} kg`,
              },
            ].map((stat) => (
              <div key={stat.label}>
                <p className="font-black text-lg text-primary">{stat.value}</p>
                <p className="text-[9px] text-muted-foreground leading-tight">
                  {stat.label}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
