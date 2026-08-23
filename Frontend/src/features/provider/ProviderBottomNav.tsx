import {
  ClipboardList,
  LayoutDashboard,
  Package,
  Store,
} from "lucide-react";
import type { ElementType } from "react";
import type { ProviderTab } from "../../lib/types";

const TABS: { id: ProviderTab; icon: ElementType; label: string }[] = [
  { id: "dashboard", icon: LayoutDashboard, label: "Inicio" },
  { id: "bags", icon: Package, label: "Mis Bolsas" },
  { id: "orders", icon: ClipboardList, label: "Pedidos" },
  { id: "store", icon: Store, label: "Mi Comercio" },
];

export default function ProviderBottomNav({
  activeTab,
  onChange,
}: {
  activeTab: ProviderTab;
  onChange: (t: ProviderTab) => void;
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
              className={isActive ? "text-primary" : "text-muted-foreground"}
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
