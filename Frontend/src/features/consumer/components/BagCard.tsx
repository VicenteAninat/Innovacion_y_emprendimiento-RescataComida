import { Clock, Heart, MapPin, Star } from "lucide-react";
import type { Bag } from "../../../lib/types";
import { fmt, savingsPct } from "../../../lib/format";

export default function BagCard({
  bag,
  onSelect,
  saved,
  onSave,
}: {
  bag: Bag;
  onSelect: (b: Bag) => void;
  saved: boolean;
  onSave: () => void;
}) {
  const pct = savingsPct(bag.price, bag.originalValue);
  return (
    <div
      className="bg-card rounded-2xl overflow-hidden border border-border cursor-pointer active:scale-[0.98] transition-transform"
      onClick={() => onSelect(bag)}
    >
      <div className="relative h-32 bg-muted">
        <img
          src={bag.image}
          alt={`Bolsa sorpresa de ${bag.restaurant}`}
          className="w-full h-full object-cover"
        />
        <button
          onClick={(e) => {
            e.stopPropagation();
            onSave();
          }}
          className="absolute top-2 right-2 w-7 h-7 rounded-full bg-white/90 flex items-center justify-center shadow-sm"
        >
          <Heart
            size={13}
            className={
              saved ? "fill-primary text-primary" : "text-muted-foreground"
            }
          />
        </button>
        <div className="absolute top-2 left-2 bg-secondary rounded-full px-2 py-0.5 shadow-sm">
          <span className="text-[9px] font-black text-foreground">
            -{pct}%
          </span>
        </div>
        {bag.remaining <= 3 && (
          <div className="absolute bottom-2 left-2 bg-primary/90 rounded-full px-2 py-0.5">
            <span className="text-[9px] font-bold text-white">
              ¡Solo {bag.remaining}!
            </span>
          </div>
        )}
      </div>
      <div className="p-3">
        <p className="font-bold text-xs text-foreground truncate">
          {bag.restaurant}
        </p>
        <p className="text-[10px] text-muted-foreground mb-2 truncate">
          {bag.type}
        </p>
        <div className="flex items-center justify-between">
          <div className="flex items-baseline gap-1">
            <span className="text-primary font-black text-[15px]">
              {fmt(bag.price)}
            </span>
            <span className="text-muted-foreground text-[9px] line-through">
              {fmt(bag.originalValue)}
            </span>
          </div>
          {bag.rating > 0 ? (
            <div className="flex items-center gap-0.5">
              <Star size={10} className="fill-yellow-400 text-yellow-400" />
              <span className="text-[10px] font-bold text-foreground">
                {bag.rating}
              </span>
            </div>
          ) : (
            <span className="text-[9px] font-bold text-muted-foreground bg-muted rounded-full px-1.5 py-0.5">
              Nuevo
            </span>
          )}
        </div>
        <div className="flex items-center gap-3 mt-1.5">
          <div className="flex items-center gap-0.5">
            <Clock size={9} className="text-muted-foreground" />
            <span className="text-[9px] text-muted-foreground">
              {bag.pickup}
            </span>
          </div>
          {bag.distance && (
            <div className="flex items-center gap-0.5 min-w-0">
              <MapPin size={9} className="text-muted-foreground shrink-0" />
              <span className="text-[9px] text-muted-foreground truncate">
                {bag.distance}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
