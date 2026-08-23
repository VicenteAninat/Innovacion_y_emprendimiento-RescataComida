import { useMemo, useState } from "react";
import { Check, ClipboardList, Clock, ShoppingBag } from "lucide-react";
import type { Offer, Reservation } from "../../lib/types";
import { fmt, formatPickupRange, timeAgo } from "../../lib/format";
import { clientAlias } from "../../lib/data/mappers";
import { updateReservationApi } from "../../lib/api/reservations";
import SectionHeader from "../shared/SectionHeader";

const STATUS_MAP: Record<
  string,
  { label: string; color: string; bg: string; next: string | null }
> = {
  pending: {
    label: "Pendiente",
    color: "text-secondary",
    bg: "bg-secondary/10",
    next: null,
  },
  paid: {
    label: "Pagado",
    color: "text-[#00C87A]",
    bg: "bg-[#00C87A]/10",
    next: "Marcar retirado",
  },
  collected: {
    label: "Retirado",
    color: "text-muted-foreground",
    bg: "bg-muted",
    next: null,
  },
  completed: {
    label: "Completado",
    color: "text-muted-foreground",
    bg: "bg-muted",
    next: null,
  },
  cancelled: {
    label: "Cancelado",
    color: "text-muted-foreground",
    bg: "bg-muted",
    next: null,
  },
};

export default function ProviderOrdersScreen({
  reservations,
  offers,
  onReload,
}: {
  reservations: Reservation[];
  offers: Offer[];
  onReload: () => void;
}) {
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<number | null>(null);

  const offerById = useMemo(
    () => new Map(offers.map((o) => [o.id ?? 0, o])),
    [offers],
  );

  const active = reservations.filter((r) => r.status !== "collected" && r.status !== "completed" && r.status !== "cancelled");
  const done = reservations.filter((r) => r.status === "collected" || r.status === "completed" || r.status === "cancelled");

  const advance = async (reservation: Reservation) => {
    setError(null);
    setBusyId(reservation.id ?? null);
    try {
      await updateReservationApi(reservation.id ?? 0, { status: "collected" });
      onReload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo actualizar.");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="pb-6">
      <div className="px-5 pt-5 pb-4">
        <h1
          className="font-black text-2xl text-foreground"
          style={{ fontFamily: "'Righteous', sans-serif" }}
        >
          Pedidos
        </h1>
      </div>

      {error && (
        <div className="mx-5 mb-4 bg-primary/10 border border-primary/20 rounded-2xl p-3.5">
          <p className="text-xs text-foreground leading-relaxed">{error}</p>
        </div>
      )}

      {active.length > 0 && (
        <>
          <SectionHeader title="Por gestionar" />
          <div className="px-5 flex flex-col gap-3 mb-5">
            {active.map((order) => {
              const s = STATUS_MAP[order.status] ?? STATUS_MAP.pending;
              const offer = offerById.get(order.offer_id);
              const busy = busyId === order.id;
              return (
                <div
                  key={order.id}
                  className="bg-card border border-border rounded-2xl overflow-hidden"
                >
                  <div className="p-4">
                    <div className="flex items-start justify-between gap-2 mb-3">
                      <div>
                        <p className="font-bold text-sm text-foreground">
                          {clientAlias(order.user_id)}
                        </p>
                        <p className="text-[10px] text-muted-foreground mt-0.5">
                          #{order.id} · {timeAgo(order.created_at)}
                        </p>
                      </div>
                      <span
                        className={`text-[10px] font-bold px-2 py-1 rounded-full ${s.bg} ${s.color} shrink-0`}
                      >
                        {s.label}
                      </span>
                    </div>
                    <div className="bg-muted rounded-xl p-2.5 mb-3 flex items-center gap-2">
                      <ShoppingBag
                        size={13}
                        className="text-muted-foreground shrink-0"
                      />
                      <div>
                        <p className="text-xs font-bold text-foreground">
                          {offer?.title ?? "Bolsa sorpresa"} × {order.quantity}
                        </p>
                        <div className="flex items-center gap-1 mt-0.5">
                          <Clock size={9} className="text-muted-foreground" />
                          <span className="text-[9px] text-muted-foreground">
                            {offer
                              ? formatPickupRange(
                                  offer.pickup_start_time,
                                  offer.pickup_end_time,
                                )
                              : "—"}
                          </span>
                        </div>
                      </div>
                      <span className="ml-auto font-black text-sm text-foreground">
                        {fmt(order.total_price ?? 0)}
                      </span>
                    </div>
                    {s.next && (
                      <button
                        onClick={() => advance(order)}
                        disabled={busy}
                        className={`w-full h-9 rounded-xl font-bold text-xs flex items-center justify-center gap-1.5 ${
                          order.status === "paid"
                            ? "bg-accent text-white"
                            : "bg-secondary text-foreground"
                        }`}
                      >
                        {busy ? (
                          <div className="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                        ) : (
                          <Check size={13} />
                        )}
                        {s.next}
                      </button>
                    )}
                    {!s.next && order.status === "pending" && (
                      <p className="text-[10px] text-muted-foreground text-center">
                        Esperando el pago del cliente (ventana de 15 min).
                      </p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </>
      )}

      {active.length === 0 && done.length === 0 && (
        <div className="flex flex-col items-center justify-center py-14 px-5">
          <ClipboardList size={36} className="text-muted-foreground mb-3" />
          <p className="text-sm text-muted-foreground text-center">
            Aún no hay pedidos para tu comercio.
          </p>
        </div>
      )}

      {done.length > 0 && (
        <>
          <SectionHeader title="Completados" />
          <div className="px-5 flex flex-col gap-2">
            {done.map((order) => {
              const offer = offerById.get(order.offer_id);
              const s = STATUS_MAP[order.status] ?? STATUS_MAP.collected;
              return (
                <div
                  key={order.id}
                  className="bg-card border border-border rounded-xl p-3 flex items-center gap-3"
                >
                  <div className="w-8 h-8 rounded-lg bg-muted flex items-center justify-center shrink-0">
                    <Check size={14} className="text-muted-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-xs text-foreground">
                      {clientAlias(order.user_id)} — {offer?.title ?? "Bolsa"}
                    </p>
                    <p className="text-[10px] text-muted-foreground">
                      #{order.id} · {timeAgo(order.created_at)} ·{" "}
                      <span className={s.color}>{s.label}</span>
                    </p>
                  </div>
                  <p className="font-black text-sm text-foreground shrink-0">
                    {fmt(order.total_price ?? 0)}
                  </p>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
