import { useState } from "react";
import { TreePine } from "lucide-react";
import type { Bag } from "../../../lib/types";
import { fmt, savingsPct } from "../../../lib/format";
import { mapPositionForId } from "../../../lib/data/mappers";

export default function MapView({
  bags,
  onSelect,
}: {
  bags: Bag[];
  onSelect: (b: Bag) => void;
}) {
  const [activePin, setActivePin] = useState<number | null>(null);

  return (
    <div
      className="mx-5 rounded-2xl overflow-hidden border border-border relative"
      style={{ height: 340 }}
      onClick={() => setActivePin(null)}
    >
      {/* Stylized map background */}
      <div className="absolute inset-0" style={{ background: "#EDE5D3" }} />
      {/* Street grid overlay */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage:
            "linear-gradient(rgba(0,0,0,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,0.06) 1px, transparent 1px)",
          backgroundSize: "28px 28px",
        }}
      />
      {/* Main avenues */}
      <div
        className="absolute bg-[#D0C0A0]"
        style={{ top: "42%", left: 0, right: 0, height: 10 }}
      />
      <div
        className="absolute bg-[#D0C0A0]"
        style={{ left: "28%", top: 0, bottom: 0, width: 8 }}
      />
      <div
        className="absolute bg-[#D0C0A0]"
        style={{ left: "64%", top: 0, bottom: 0, width: 6 }}
      />
      {/* Secondary streets */}
      <div
        className="absolute bg-[#D8CEB8]"
        style={{ top: "22%", left: 0, right: 0, height: 4 }}
      />
      <div
        className="absolute bg-[#D8CEB8]"
        style={{ top: "70%", left: 0, right: 0, height: 4 }}
      />
      <div
        className="absolute bg-[#D8CEB8]"
        style={{ left: "46%", top: 0, bottom: 0, width: 4 }}
      />
      {/* Park */}
      <div
        className="absolute bg-[#BDD9A4] rounded-sm"
        style={{ left: "48%", top: "46%", width: "14%", height: "20%" }}
      >
        <div className="w-full h-full flex items-center justify-center opacity-50">
          <TreePine size={12} className="text-foreground" />
        </div>
      </div>
      {/* City blocks */}
      {[
        { l: "29%", t: "23%", w: "17%", h: "18%" },
        { l: "47%", t: "23%", w: "16%", h: "18%" },
        { l: "65%", t: "23%", w: "18%", h: "18%" },
        { l: "29%", t: "47%", w: "17%", h: "22%" },
        { l: "65%", t: "47%", w: "18%", h: "22%" },
        { l: "0%", t: "23%", w: "27%", h: "18%" },
        { l: "0%", t: "47%", w: "27%", h: "22%" },
      ].map((b, i) => (
        <div
          key={i}
          className="absolute bg-[#D9CEB8] rounded-sm opacity-60"
          style={{ left: b.l, top: b.t, width: b.w, height: b.h }}
        />
      ))}

      {/* User location */}
      <div className="absolute" style={{ left: "50%", top: "50%", zIndex: 10 }}>
        <div className="w-12 h-12 rounded-full bg-blue-500/20 absolute -translate-x-1/2 -translate-y-1/2" />
        <div className="w-4 h-4 rounded-full bg-blue-500 border-2 border-white shadow-lg absolute -translate-x-1/2 -translate-y-1/2" />
      </div>

      {/* Restaurant pins */}
      {bags.map((bag) => {
        const pos = mapPositionForId(bag.id);
        const isActive = activePin === bag.id;
        const pct = savingsPct(bag.price, bag.originalValue);

        return (
          <div
            key={bag.id}
            className="absolute"
            style={{
              left: `${pos.x}%`,
              top: `${pos.y}%`,
              zIndex: isActive ? 30 : 20,
            }}
          >
            {/* Popup card */}
            {isActive && (
              <div
                className="absolute z-30 bg-card rounded-2xl shadow-xl border border-border overflow-hidden w-44"
                style={{
                  bottom: "calc(100% + 6px)",
                  left: "50%",
                  transform: "translateX(-50%)",
                }}
                onClick={(e) => e.stopPropagation()}
              >
                <div className="h-20 bg-muted relative">
                  <img
                    src={bag.image}
                    alt={bag.restaurant}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute top-1.5 left-1.5 bg-secondary rounded-full px-1.5 py-0.5">
                    <span className="text-[9px] font-black text-foreground">
                      -{pct}%
                    </span>
                  </div>
                </div>
                <div className="p-2.5">
                  <p className="font-bold text-xs text-foreground truncate">
                    {bag.restaurant}
                  </p>
                  <p className="text-[9px] text-muted-foreground mb-1.5">
                    {[bag.distance, bag.pickup].filter(Boolean).join(" · ")}
                  </p>
                  <button
                    onClick={() => {
                      onSelect(bag);
                      setActivePin(null);
                    }}
                    className="w-full bg-primary text-white text-xs font-bold py-1.5 rounded-xl"
                  >
                    {fmt(bag.price)} — Ver bolsa
                  </button>
                </div>
              </div>
            )}

            {/* Pin button */}
            <button
              onClick={(e) => {
                e.stopPropagation();
                setActivePin(isActive ? null : bag.id);
              }}
              className={`px-2.5 py-1 rounded-full text-xs font-black shadow-lg transition-all -translate-x-1/2 -translate-y-full block ${
                isActive
                  ? "bg-primary text-white scale-110"
                  : "bg-white text-foreground border border-border"
              }`}
            >
              {fmt(bag.price)}
            </button>
          </div>
        );
      })}

      {/* Attribution */}
      <div className="absolute bottom-2 right-2 bg-white/70 rounded px-1.5 py-0.5 z-10">
        <span className="text-[8px] text-muted-foreground">
          Providencia, Santiago
        </span>
      </div>
    </div>
  );
}
