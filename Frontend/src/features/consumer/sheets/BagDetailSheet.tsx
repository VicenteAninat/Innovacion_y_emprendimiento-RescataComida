import { useEffect, useState } from "react";
import { ArrowLeft, Clock, Heart, Leaf, MapPin, Star } from "lucide-react";
import type { Bag, ReviewView } from "../../../lib/types";
import { fmt, savingsPct } from "../../../lib/format";
import { getBusinessReviewsCached } from "../../../lib/data/cache";
import { reviewToView } from "../../../lib/data/mappers";

export default function BagDetailSheet({
  bag,
  onClose,
  onOpenPayment,
  saved,
  onToggleSave,
}: {
  bag: Bag;
  onClose: () => void;
  onOpenPayment: () => void;
  saved: boolean;
  onToggleSave: () => void;
}) {
  const [reviews, setReviews] = useState<ReviewView[]>([]);
  const pct = savingsPct(bag.price, bag.originalValue);
  const savedMoney = (bag.originalValue - bag.price).toLocaleString("es-CL", {
    maximumFractionDigits: 0,
  });

  useEffect(() => {
    let cancelled = false;
    getBusinessReviewsCached(bag.restaurantId).then((list) => {
      if (!cancelled) setReviews(list.map(reviewToView));
    });
    return () => {
      cancelled = true;
    };
  }, [bag.restaurantId]);

  return (
    <div className="absolute inset-0 flex flex-col" style={{ zIndex: 50 }}>
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="absolute bottom-0 left-0 right-0 bg-background rounded-t-3xl overflow-hidden flex flex-col max-h-[92%]">
        {/* Image header */}
        <div className="relative h-52 bg-muted shrink-0">
          <img
            src={bag.image}
            alt={`Bolsa sorpresa de ${bag.restaurant}`}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
          <button
            onClick={onClose}
            className="absolute top-4 left-4 w-9 h-9 rounded-full bg-black/40 flex items-center justify-center"
          >
            <ArrowLeft size={18} className="text-white" />
          </button>
          <button
            onClick={onToggleSave}
            className="absolute top-4 right-4 w-9 h-9 rounded-full bg-black/40 flex items-center justify-center"
          >
            <Heart
              size={18}
              className={saved ? "fill-primary text-primary" : "text-white"}
            />
          </button>
          <div className="absolute bottom-4 left-4 right-4 flex items-end justify-between">
            <div>
              <p className="text-white font-bold text-lg leading-tight">
                {bag.restaurant}
              </p>
              <div className="flex items-center gap-1 mt-0.5">
                {bag.rating > 0 ? (
                  <>
                    <Star size={11} className="fill-yellow-400 text-yellow-400" />
                    <span className="text-white text-xs font-bold">
                      {bag.rating}
                    </span>
                    <span className="text-white/60 text-xs">
                      ({bag.reviews} reseñas)
                    </span>
                  </>
                ) : (
                  <span className="text-white/60 text-xs">Sin reseñas aún</span>
                )}
              </div>
            </div>
            <div className="bg-secondary rounded-full px-2.5 py-0.5 shadow-sm">
              <span className="font-black text-sm text-foreground">
                -{pct}%
              </span>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {/* Price */}
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-[11px] text-muted-foreground mb-0.5">
                {bag.type}
              </p>
              <div className="flex items-baseline gap-2">
                <span className="text-primary font-black text-3xl">
                  {fmt(bag.price)}
                </span>
                <span className="text-muted-foreground text-sm line-through">
                  {fmt(bag.originalValue)}
                </span>
              </div>
              <p className="text-accent text-xs font-bold mt-0.5">
                Ahorras ${savedMoney}
              </p>
            </div>
            <div className="bg-primary/10 rounded-2xl px-3 py-2 text-center">
              <p className="text-primary font-black text-xl leading-none">
                {bag.remaining}
              </p>
              <p className="text-primary/60 text-[10px] mt-0.5">
                disponibles
              </p>
            </div>
          </div>

          <p className="text-sm text-muted-foreground leading-relaxed mb-4">
            {bag.description}
          </p>

          <div className="flex gap-2 flex-wrap mb-4">
            {bag.tags.map((tag) => (
              <span
                key={tag}
                className="bg-muted text-muted-foreground text-xs font-semibold px-3 py-1 rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>

          {/* Pickup & distance */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className="bg-muted rounded-2xl p-3">
              <p className="text-[10px] text-muted-foreground mb-1.5">
                Horario de retiro
              </p>
              <div className="flex items-center gap-1.5">
                <Clock size={13} className="text-foreground shrink-0" />
                <span className="text-sm font-bold text-foreground">
                  {bag.pickup}
                </span>
              </div>
            </div>
            <div className="bg-muted rounded-2xl p-3">
              <p className="text-[10px] text-muted-foreground mb-1.5">
                Ubicación
              </p>
              <div className="flex items-center gap-1.5">
                <MapPin size={13} className="text-foreground shrink-0" />
                <span className="text-sm font-bold text-foreground truncate">
                  {bag.distance ?? "Consultar en local"}
                </span>
              </div>
            </div>
          </div>

          {/* Eco impact */}
          <div className="bg-accent/10 border border-accent/20 rounded-2xl p-3.5 mb-5">
            <div className="flex items-center gap-2.5">
              <Leaf size={16} className="text-accent shrink-0" />
              <div>
                <p className="text-xs font-bold text-foreground">
                  Impacto ambiental
                </p>
                <p className="text-[10px] text-muted-foreground mt-0.5">
                  Rescatando esta bolsa evitas {bag.co2Saved} kg de CO₂ y
                  salvas {bag.kgSaved} kg de alimento
                </p>
              </div>
            </div>
          </div>

          {/* Reviews section */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <p
                className="font-bold text-sm text-foreground"
                style={{ fontFamily: "'Righteous', sans-serif" }}
              >
                Reseñas {reviews.length > 0 && `(${reviews.length})`}
              </p>
              {reviews.length > 0 && bag.rating > 0 && (
                <div className="flex items-center gap-1">
                  <Star size={11} className="fill-yellow-400 text-yellow-400" />
                  <span className="text-xs font-black text-foreground">
                    {bag.rating}
                  </span>
                  <span className="text-xs text-muted-foreground">/ 5</span>
                </div>
              )}
            </div>

            {reviews.length > 0 ? (
              <div className="flex flex-col gap-3 mb-4">
                {reviews.map((r, i) => (
                  <div key={i} className="bg-muted rounded-2xl p-3">
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-full bg-primary flex items-center justify-center text-white text-[10px] font-black">
                          {r.user[0]}
                        </div>
                        <span className="text-xs font-bold text-foreground">
                          {r.user}
                        </span>
                      </div>
                      <div className="flex items-center gap-0.5">
                        {Array.from({ length: r.rating }).map((_, j) => (
                          <Star
                            key={j}
                            size={9}
                            className="fill-yellow-400 text-yellow-400"
                          />
                        ))}
                      </div>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      {r.text}
                    </p>
                    <p className="text-[9px] text-muted-foreground/60 mt-1">
                      {r.date}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-muted rounded-2xl p-6 text-center mb-4">
                <Star size={28} className="text-muted-foreground mx-auto mb-2" />
                <p className="text-sm font-bold text-foreground mb-1">
                  Aún no hay reseñas
                </p>
                <p className="text-xs text-muted-foreground">
                  Las reseñas aparecerán aquí
                </p>
              </div>
            )}
          </div>
        </div>

        {/* CTA */}
        <div className="px-5 pb-6 pt-3 border-t border-border shrink-0">
          <button
            onClick={onOpenPayment}
            disabled={bag.remaining <= 0}
            className={`w-full h-14 rounded-2xl font-bold text-base active:scale-[0.98] transition-transform ${
              bag.remaining > 0
                ? "bg-primary text-white"
                : "bg-muted text-muted-foreground"
            }`}
          >
            {bag.remaining > 0
              ? `Reservar por ${fmt(bag.price)}`
              : "Agotada"}
          </button>
        </div>
      </div>
    </div>
  );
}
