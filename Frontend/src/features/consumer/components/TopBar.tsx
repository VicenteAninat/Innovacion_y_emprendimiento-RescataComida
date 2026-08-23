import { Bell, ChevronRight, MapPin } from "lucide-react";

export default function TopBar() {
  return (
    <div className="flex items-center justify-between px-5 pt-5 pb-3">
      <div>
        <p className="text-[10px] text-muted-foreground font-semibold tracking-widest uppercase">
          Tu ubicación
        </p>
        <button className="flex items-center gap-1 mt-0.5">
          <MapPin size={13} className="text-primary" />
          <span className="font-bold text-sm text-foreground">
            Santiago, Providencia
          </span>
          <ChevronRight size={13} className="text-muted-foreground" />
        </button>
      </div>
      <button className="relative w-10 h-10 rounded-full bg-card border border-border flex items-center justify-center">
        <Bell size={18} className="text-foreground" />
        <span className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full ring-2 ring-background" />
      </button>
    </div>
  );
}
