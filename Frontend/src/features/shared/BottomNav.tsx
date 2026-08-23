import { Compass, Home, Package, User } from "lucide-react";
import type { Tab } from "../../lib/types";

const TABS = [
  { id: "home" as Tab, icon: Home, label: "Inicio" },
  { id: "explore" as Tab, icon: Compass, label: "Explorar" },
  { id: "orders" as Tab, icon: Package, label: "Pedidos" },
  { id: "profile" as Tab, icon: User, label: "Perfil" },
];

export default function BottomNav({
  activeTab,
  onChange,
}: {
  activeTab: Tab;
  onChange: (t: Tab) => void;
}) {
  return (
    <div className="border-t border-border bg-card flex items-center shrink-0">
      {TABS.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className="flex-1 flex flex-col items-center gap-0.5 py-3"
          >
            <Icon
              size={22}
              className={
                isActive ? "text-primary" : "text-muted-foreground"
              }
              strokeWidth={isActive ? 2.5 : 1.8}
            />
            <span
              className={`text-[9px] font-bold ${
                isActive ? "text-primary" : "text-muted-foreground"
              }`}
            >
              {tab.label}
            </span>
          </button>
        );
      })}
    </div>
  );
}
