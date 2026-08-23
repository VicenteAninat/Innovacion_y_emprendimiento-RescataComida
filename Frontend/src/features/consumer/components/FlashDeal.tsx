import { Clock, Zap } from "lucide-react";
import type { Bag } from "../../../lib/types";
import { fmt, savingsPct } from "../../../lib/format";
import { useCountdown } from "../../../lib/hooks/useCountdown";

export default function FlashDeal({
  bag,
  onSelect,
}: {
  bag: Bag;
  onSelect: (b: Bag) => void;
}) {
  const countdown = useCountdown(new Date(bag.pickupEnd).getTime());
  const pct = savingsPct(bag.price, bag.originalValue);

  return (
    <div
      onClick={() => onSelect(bag)}
      className="mx-5 mb-5 rounded-3xl overflow-hidden cursor-pointer relative select-none"
      style={{ background: "#FF4422" }}
    >
      <div className="absolute top-3 right-16 w-14 h-14 rounded-full bg-white/10 pointer-events-none" />
      <div className="absolute -top-1 right-10 w-5 h-5 rounded-full bg-yellow-300/30 pointer-events-none" />
      <div className="absolute bottom-6 right-24 w-3 h-3 bg-white/20 rotate-45 pointer-events-none" />
      <div className="absolute top-1/2 left-1 w-10 h-10 rounded-full bg-white/5 pointer-events-none" />

      <div className="flex items-stretch">
        <div className="flex-1 p-4 z-10">
          <div className="flex items-center gap-1.5 mb-2">
            <Zap size={11} fill="currentColor" className="text-yellow-300" />
            <span className="text-[9px] font-black tracking-widest text-yellow-300 uppercase">
              Oferta Relámpago
            </span>
          </div>
          <p className="text-white font-bold text-[15px] leading-tight mb-0.5">
            {bag.restaurant}
          </p>
          <p className="text-white/70 text-[11px] mb-3">{bag.type}</p>
          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-white text-2xl font-black">
              {fmt(bag.price)}
            </span>
            <span className="text-white/55 text-xs line-through">
              {fmt(bag.originalValue)}
            </span>
          </div>
          <div className="flex items-center gap-1.5 bg-black/25 rounded-full px-2.5 py-1 w-fit">
            <Clock size={9} className="text-yellow-300" />
            <span className="text-yellow-300 text-[11px] font-black font-mono tracking-wider">
              {countdown}
            </span>
          </div>
        </div>
        <div className="w-28 relative shrink-0">
          <img
            src={bag.image}
            alt={`Bolsa sorpresa de ${bag.restaurant}`}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-l from-transparent to-[#FF4422]/50" />
          <div className="absolute top-2 right-2 bg-secondary rounded-full px-1.5 py-0.5 shadow-sm">
            <span className="text-[10px] font-black text-foreground">
              -{pct}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
