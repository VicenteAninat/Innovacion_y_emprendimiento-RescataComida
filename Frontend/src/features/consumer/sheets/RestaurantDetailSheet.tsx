import { useEffect, useState } from "react";
import { ArrowLeft, Clock, MapPin, Star } from "lucide-react";
import type { Bag, Restaurant, ReviewView } from "../../../lib/types";
import { fmt, savingsPct } from "../../../lib/format";
import { getBusinessReviewsCached } from "../../../lib/data/cache";
import { reviewToView } from "../../../lib/data/mappers";

export default function RestaurantDetailSheet({
  restaurant,
  onClose,
  onSelectBag,
}: {
  restaurant: Restaurant;
  onClose: () => void;
  onSelectBag: (bag: Bag) => void;
}) {
  const [reviews, setReviews] = useState<ReviewView[]>([]);

  useEffect(() => {
    let cancelled = false;
    getBusinessReviewsCached(restaurant.id).then((list) => {
      if (!cancelled) setReviews(list.map(reviewToView));
    });
    return () => {
      cancelled = true;
    };
  }, [restaurant.id]);

  return (
    <div className="absolute inset-0 flex flex-col" style={{ zIndex: 50 }}>
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="absolute bottom-0 left-0 right-0 bg-background rounded-t-3xl overflow-hidden flex flex-col max-h-[92%]">
        {/* Header */}
        <div className="relative h-52 bg-muted shrink-0">
          <img
            src={restaurant.image}
            alt={restaurant.name}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
          <button
            onClick={onClose}
            className="absolute top-4 left-4 w-9 h-9 rounded-full bg-black/40 flex items-center justify-center"
          >
            <ArrowLeft size={18} className="text-white" />
          </button>
          <div className="absolute bottom-4 left-4 right-4">
            <p className="text-white font-bold text-xl leading-tight mb-1">
              {restaurant.name}
            </p>
            <div className="flex items-center gap-1">
              {restaurant.rating > 0 ? (
                <>
                  <Star size={11} className="fill-yellow-400 text-yellow-400" />
                  <span className="text-white text-xs font-bold">
                    {restaurant.rating}
                  </span>
                  <span className="text-white/60 text-xs">
                    ({restaurant.reviews} reseñas)
                  </span>
                </>
              ) : (
                <span className="text-white/60 text-xs">
                  Sin reseñas aún
                </span>
              )}
              {restaurant.distance && (
                <>
                  <span className="text-white/60 text-xs mx-1">·</span>
                  <MapPin size={11} className="text-white/60" />
                  <span className="text-white/60 text-xs">
                    {restaurant.distance}
                  </span>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {/* Available bags section */}
          <div className="mb-5">
            <div className="flex items-center justify-between mb-3">
              <p
                className="font-bold text-base text-foreground"
                style={{ fontFamily: "'Righteous', sans-serif" }}
              >
                Bolsas disponibles
              </p>
              <span className="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded-full">
                {restaurant.bags.length}{" "}
                {restaurant.bags.length === 1 ? "opción" : "opciones"}
              </span>
            </div>
            <div className="flex flex-col gap-3">
              {restaurant.bags.map((bag) => {
                const pct = savingsPct(bag.price, bag.originalValue);
                return (
                  <div
                    key={bag.id}
                    onClick={() => onSelectBag(bag)}
                    className="bg-card rounded-2xl border border-border overflow-hidden cursor-pointer active:scale-[0.99] transition-transform"
                  >
                    <div className="flex">
                      <div className="w-24 h-24 shrink-0 relative bg-muted">
                        <img
                          src={bag.image}
                          alt={bag.type}
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute top-1.5 left-1.5 bg-secondary rounded-full px-1.5 py-0.5">
                          <span className="text-[9px] font-black text-foreground">
                            -{pct}%
                          </span>
                        </div>
                      </div>
                      <div className="flex-1 p-3 min-w-0">
                        <p className="font-bold text-sm text-foreground mb-0.5">
                          {bag.type}
                        </p>
                        <div className="flex items-center gap-1 mb-2">
                          <Clock size={9} className="text-muted-foreground" />
                          <span className="text-[9px] text-muted-foreground">
                            {bag.pickup}
                          </span>
                          {bag.remaining <= 3 && (
                            <>
                              <span className="text-muted-foreground text-[9px] mx-0.5">
                                ·
                              </span>
                              <span className="text-[9px] font-bold text-primary">
                                ¡Solo {bag.remaining}!
                              </span>
                            </>
                          )}
                        </div>
                        <div className="flex items-baseline gap-1.5">
                          <span className="text-primary font-black text-lg">
                            {fmt(bag.price)}
                          </span>
                          <span className="text-muted-foreground text-[10px] line-through">
                            {fmt(bag.originalValue)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Reviews section */}
          {reviews.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-3">
                <p
                  className="font-bold text-sm text-foreground"
                  style={{ fontFamily: "'Righteous', sans-serif" }}
                >
                  Reseñas ({reviews.length})
                </p>
                {restaurant.rating > 0 && (
                  <div className="flex items-center gap-1">
                    <Star
                      size={11}
                      className="fill-yellow-400 text-yellow-400"
                    />
                    <span className="text-xs font-black text-foreground">
                      {restaurant.rating}
                    </span>
                    <span className="text-xs text-muted-foreground">/ 5</span>
                  </div>
                )}
              </div>
              <div className="flex flex-col gap-3">
                {reviews.slice(0, 3).map((r, i) => (
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
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
