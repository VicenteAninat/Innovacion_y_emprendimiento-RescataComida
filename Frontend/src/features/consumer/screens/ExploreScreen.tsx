import { useMemo, useState } from "react";
import { Clock, Heart, List, Map as MapIcon, MapPin, Star } from "lucide-react";
import type { Bag } from "../../../lib/types";
import { fmt, savingsPct } from "../../../lib/format";
import SearchBar from "../../shared/SearchBar";
import MapView from "../components/MapView";

type SortBy = "price" | "distance" | "rating";

export default function ExploreScreen({
  bags,
  onSelectBag,
  favoriteIds,
  onToggleFavorite,
}: {
  bags: Bag[];
  onSelectBag: (b: Bag) => void;
  favoriteIds: Set<number>;
  onToggleFavorite: (businessId: number) => void;
}) {
  const [sortBy, setSortBy] = useState<SortBy>("price");
  const [viewMode, setViewMode] = useState<"list" | "map">("list");

  const sorted = useMemo(() => {
    return [...bags].sort((a, b) => {
      if (sortBy === "price") return a.price - b.price;
      if (sortBy === "rating") return b.rating - a.rating;
      const aDist = a.distance ? parseFloat(a.distance) : Infinity;
      const bDist = b.distance ? parseFloat(b.distance) : Infinity;
      return aDist - bDist;
    });
  }, [bags, sortBy]);

  return (
    <div className="pb-6">
      <div className="px-5 pt-5 pb-3">
        <div className="flex items-center justify-between mb-4">
          <h1
            className="font-black text-2xl text-foreground"
            style={{ fontFamily: "'Righteous', sans-serif" }}
          >
            Explorar
          </h1>
          {/* List / Map toggle */}
          <div className="flex bg-muted rounded-xl p-0.5 gap-0.5">
            <button
              onClick={() => setViewMode("list")}
              className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === "list"
                  ? "bg-card shadow-sm text-foreground"
                  : "text-muted-foreground"
              }`}
            >
              <List size={13} />
              Lista
            </button>
            <button
              onClick={() => setViewMode("map")}
              className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === "map"
                  ? "bg-card shadow-sm text-foreground"
                  : "text-muted-foreground"
              }`}
            >
              <MapIcon size={13} />
              Mapa
            </button>
          </div>
        </div>
        <SearchBar placeholder="Buscar por zona o restaurante..." />
      </div>

      {viewMode === "map" ? (
        <>
          <MapView bags={bags} onSelect={onSelectBag} />
          <div className="px-5 mt-4">
            <p className="text-xs text-muted-foreground text-center">
              Toca un pin para ver la bolsa disponible
            </p>
          </div>
        </>
      ) : (
        <>
          <div className="flex gap-2 px-5 pb-4">
            {(["price", "distance", "rating"] as const).map((s) => (
              <button
                key={s}
                onClick={() => setSortBy(s)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all ${
                  sortBy === s
                    ? "bg-foreground text-background border-foreground"
                    : "bg-card border-border text-foreground"
                }`}
              >
                {s === "price"
                  ? "Precio"
                  : s === "distance"
                    ? "Distancia"
                    : "Valoración"}
              </button>
            ))}
          </div>

          <div className="px-5 flex flex-col gap-3">
            {sorted.map((bag) => {
              const pct = savingsPct(bag.price, bag.originalValue);
              return (
                <div
                  key={bag.id}
                  onClick={() => onSelectBag(bag)}
                  className="bg-card rounded-2xl flex overflow-hidden border border-border cursor-pointer active:scale-[0.99] transition-transform"
                >
                  <div className="w-28 shrink-0 relative bg-muted">
                    <img
                      src={bag.image}
                      alt={`Bolsa de ${bag.restaurant}`}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute top-1.5 left-1.5 bg-secondary rounded-full px-1.5 py-0.5">
                      <span className="text-[9px] font-black text-foreground">
                        -{pct}%
                      </span>
                    </div>
                  </div>
                  <div className="flex-1 p-3 min-w-0">
                    <p className="font-bold text-sm text-foreground truncate">
                      {bag.restaurant}
                    </p>
                    <p className="text-[11px] text-muted-foreground mb-1 truncate">
                      {bag.type}
                    </p>
                    <div className="flex items-center gap-1 mb-1.5">
                      {bag.rating > 0 ? (
                        <>
                          <Star
                            size={10}
                            className="fill-yellow-400 text-yellow-400 shrink-0"
                          />
                          <span className="text-[10px] font-bold">
                            {bag.rating}
                          </span>
                          <span className="text-[10px] text-muted-foreground">
                            ({bag.reviews})
                          </span>
                        </>
                      ) : (
                        <span className="text-[10px] font-bold text-muted-foreground">
                          Sin reseñas aún
                        </span>
                      )}
                      {bag.distance && (
                        <>
                          <span className="text-muted-foreground text-[10px] mx-0.5">
                            ·
                          </span>
                          <MapPin
                            size={9}
                            className="text-muted-foreground shrink-0"
                          />
                          <span className="text-[10px] text-muted-foreground truncate">
                            {bag.distance}
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
                    <div className="flex items-center gap-0.5 mt-0.5">
                      <Clock size={9} className="text-muted-foreground" />
                      <span className="text-[9px] text-muted-foreground">
                        {bag.pickup}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onToggleFavorite(bag.restaurantId);
                    }}
                    className="flex items-center justify-center w-12 border-l border-border shrink-0"
                  >
                    <Heart
                      size={16}
                      className={
                        favoriteIds.has(bag.restaurantId)
                          ? "fill-primary text-primary"
                          : "text-muted-foreground"
                      }
                    />
                  </button>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
