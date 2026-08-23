import { LayoutGrid, type LucideIcon } from "lucide-react";
import type { Bag } from "../../../lib/types";
import { categoryIcon, categoryLabel } from "../../../lib/images";

export interface CategoryOption {
  id: string;
  label: string;
  icon: LucideIcon;
}

/** Construye las pills de categorías a partir de las bolsas disponibles. */
export function buildCategoryOptions(bags: Bag[]): CategoryOption[] {
  const seen = new Set<string>();
  const options: CategoryOption[] = [
    { id: "all", label: "Todos", icon: LayoutGrid },
  ];
  for (const bag of bags) {
    const cat = bag.category || "other";
    if (seen.has(cat)) continue;
    seen.add(cat);
    options.push({
      id: cat,
      label: categoryLabel(cat),
      icon: categoryIcon(cat),
    });
  }
  return options;
}

export default function CategoryPills({
  active,
  onChange,
  options,
}: {
  active: string;
  onChange: (id: string) => void;
  options: CategoryOption[];
}) {
  return (
    <div className="flex gap-2 overflow-x-auto px-5 pb-4 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
      {options.map((cat) => {
        const Icon = cat.icon;
        return (
          <button
            key={cat.id}
            onClick={() => onChange(cat.id)}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-full whitespace-nowrap text-xs font-bold transition-all shrink-0 ${
              active === cat.id
                ? "bg-primary text-primary-foreground shadow-sm"
                : "bg-card border border-border text-foreground"
            }`}
          >
            <Icon size={14} />
            <span>{cat.label}</span>
          </button>
        );
      })}
    </div>
  );
}
