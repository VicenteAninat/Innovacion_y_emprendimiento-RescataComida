import { useState } from "react";
import {
  AlertCircle,
  Clock,
  Pencil,
  Plus,
  ShoppingBag,
  ToggleLeft,
  ToggleRight,
  Trash2,
} from "lucide-react";
import type { Business, Offer } from "../../lib/types";
import { fmt, formatPickupRange } from "../../lib/format";
import { categoryIcon } from "../../lib/images";
import { deleteOfferApi, updateOfferApi } from "../../lib/api/offers";

export default function ProviderBagsScreen({
  business,
  offers,
  onPublish,
  onEdit,
  onReload,
}: {
  business: Business;
  offers: Offer[];
  onPublish: () => void;
  onEdit: (offer: Offer) => void;
  onReload: () => void;
}) {
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<number | null>(null);

  const toggleActive = async (offer: Offer) => {
    setError(null);
    setBusyId(offer.id ?? null);
    try {
      const nextStatus = offer.status === "active" ? "inactive" : "active";
      await updateOfferApi(offer.id ?? 0, { status: nextStatus });
      onReload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo actualizar.");
    } finally {
      setBusyId(null);
    }
  };

  const removeOffer = async (offer: Offer) => {
    if (!window.confirm(`¿Eliminar la bolsa "${offer.title}"?`)) return;
    setError(null);
    setBusyId(offer.id ?? null);
    try {
      await deleteOfferApi(offer.id ?? 0);
      onReload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo eliminar.");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="pb-6">
      <div className="px-5 pt-5 pb-4 flex items-center justify-between">
        <h1
          className="font-black text-2xl text-foreground"
          style={{ fontFamily: "'Righteous', sans-serif" }}
        >
          Mis Bolsas
        </h1>
        <button
          onClick={onPublish}
          className="w-10 h-10 rounded-full bg-primary flex items-center justify-center"
        >
          <Plus size={18} className="text-white" />
        </button>
      </div>

      {error && (
        <div className="mx-5 mb-4 bg-primary/10 border border-primary/20 rounded-2xl p-3.5">
          <p className="text-xs text-foreground leading-relaxed">{error}</p>
        </div>
      )}

      <div className="px-5 flex flex-col gap-3">
        {offers.map((offer) => {
          const active = offer.status === "active";
          const CategoryIcon = categoryIcon(business.category);
          const pct = offer.original_price
            ? Math.round(
                (offer.discounted_price / offer.original_price) * 100,
              )
            : 0;
          const soldOut = (offer.quantity_available ?? 0) === 0;
          const busy = busyId === offer.id;
          return (
            <div
              key={offer.id}
              className={`rounded-2xl border overflow-hidden transition-opacity ${
                active
                  ? "bg-card border-border"
                  : "bg-muted border-border opacity-60"
              }`}
            >
              {/* Top row */}
              <div className="p-4 pb-3">
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                    <CategoryIcon size={22} className="text-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-sm text-foreground truncate">
                      {offer.title}
                    </p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <Clock size={10} className="text-muted-foreground" />
                      <span className="text-[10px] text-muted-foreground">
                        {formatPickupRange(
                          offer.pickup_start_time,
                          offer.pickup_end_time,
                        )}
                      </span>
                    </div>
                    <div className="flex items-baseline gap-1.5 mt-1">
                      <span className="text-primary font-black text-sm">
                        {fmt(offer.discounted_price)}
                      </span>
                      <span className="text-muted-foreground text-[10px] line-through">
                        {fmt(offer.original_price)}
                      </span>
                      <span className="text-[9px] font-bold bg-primary/10 text-primary rounded-full px-1.5 py-0.5">
                        -{100 - pct}%
                      </span>
                    </div>
                  </div>
                  {/* Active toggle */}
                  <button
                    onClick={() => toggleActive(offer)}
                    disabled={busy}
                    className="shrink-0 mt-1"
                  >
                    {busy ? (
                      <div className="w-7 h-7 rounded-full border-2 border-muted-foreground/30 border-t-muted-foreground animate-spin" />
                    ) : active ? (
                      <ToggleRight size={28} className="text-accent" />
                    ) : (
                      <ToggleLeft size={28} className="text-muted-foreground" />
                    )}
                  </button>
                </div>
              </div>

              {/* Bottom bar */}
              <div className="border-t border-border px-4 py-2.5 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {soldOut ? (
                    <span className="text-[10px] font-bold text-primary bg-primary/10 rounded-full px-2 py-0.5">
                      Agotada
                    </span>
                  ) : (
                    <span className="text-[10px] text-muted-foreground">
                      <span className="font-black text-foreground">
                        {offer.quantity_available}
                      </span>{" "}
                      disponibles
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onEdit(offer)}
                    className="w-7 h-7 rounded-lg bg-muted flex items-center justify-center"
                  >
                    <Pencil size={12} className="text-muted-foreground" />
                  </button>
                  <button
                    onClick={() => removeOffer(offer)}
                    className="w-7 h-7 rounded-lg bg-primary/10 flex items-center justify-center"
                  >
                    <Trash2 size={12} className="text-primary" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
        {offers.length === 0 && (
          <div className="flex flex-col items-center justify-center py-14 px-5">
            <ShoppingBag size={36} className="text-muted-foreground mb-3" />
            <p className="text-sm text-muted-foreground text-center">
              Aún no has publicado bolsas. ¡Publica tu primera bolsa sorpresa!
            </p>
          </div>
        )}
      </div>

      {/* Tip */}
      <div className="mx-5 mt-5 bg-secondary/10 border border-secondary/20 rounded-2xl p-3.5 flex items-start gap-2">
        <AlertCircle size={14} className="text-secondary shrink-0 mt-0.5" />
        <p className="text-[11px] text-foreground/70 leading-relaxed">
          Las bolsas se desactivan automáticamente cuando se agotan o vence la
          ventana de retiro.
        </p>
      </div>
    </div>
  );
}
