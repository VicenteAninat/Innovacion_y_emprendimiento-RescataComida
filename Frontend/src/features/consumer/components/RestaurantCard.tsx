import { MapPin, Star } from "lucide-react";
import type { Restaurant } from "../../../lib/types";
import { fmt } from "../../../lib/format";

export default function RestaurantCard({
  restaurant,
  onSelect,
}: {
  restaurant: Restaurant;
  onSelect: (r: Restaurant) => void;
}) {
  const minPrice = Math.min(...restaurant.bags.map((b) => b.price));
  const totalRemaining = restaurant.bags.reduce(
    (sum, b) => sum + b.remaining,
    0,
  );

  return (
    <div
      className="bg-card rounded-2xl overflow-hidden border-2 border-primary/20 cursor-pointer active:scale-[0.98] transition-transform"
      onClick={() => onSelect(restaurant)}
    >
      <div className="relative h-32 bg-muted">
        <img
          src={restaurant.image}
          alt={restaurant.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute top-2 left-2 bg-primary rounded-full px-2 py-0.5 shadow-sm">
          <span className="text-[9px] font-black text-white">
            {restaurant.bags.length} bolsas
          </span>
        </div>
        <div className="absolute bottom-2 left-2 bg-background/90 rounded-full px-2 py-0.5 backdrop-blur-sm">
          <span className="text-[9px] font-bold text-foreground">
            {totalRemaining} disponibles
          </span>
        </div>
      </div>
      <div className="p-3">
        <p className="font-bold text-xs text-foreground truncate">
          {restaurant.name}
        </p>
        <p className="text-[10px] text-muted-foreground mb-2">
          Varias opciones disponibles
        </p>
        <div className="flex items-center justify-between">
          <div className="flex items-baseline gap-1">
            <span className="text-[10px] text-muted-foreground">Desde</span>
            <span className="text-primary font-black text-[15px]">
              {fmt(minPrice)}
            </span>
          </div>
          {restaurant.rating > 0 ? (
            <div className="flex items-center gap-0.5">
              <Star size={10} className="fill-yellow-400 text-yellow-400" />
              <span className="text-[10px] font-bold text-foreground">
                {restaurant.rating}
              </span>
            </div>
          ) : (
            <span className="text-[9px] font-bold text-muted-foreground bg-muted rounded-full px-2 py-0.5">
              Nuevo
            </span>
          )}
        </div>
        {restaurant.distance && (
          <div className="flex items-center gap-0.5 mt-1.5">
            <MapPin size={9} className="text-muted-foreground" />
            <span className="text-[9px] text-muted-foreground truncate">
              {restaurant.distance}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
