// ─── METADATOS DE CATEGORÍAS E IMÁGENES (el backend no guarda imágenes) ──────

import {
  Coffee,
  Croissant,
  Fish,
  ShoppingBasket,
  Store,
  Utensils,
  type LucideIcon,
} from "lucide-react";

export interface CategoryMeta {
  label: string;
  icon: LucideIcon;
  image: string;
}

export const DEFAULT_CATEGORY_META: CategoryMeta = {
  label: "Comercio",
  icon: Store,
  image:
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop&auto=format",
};

const CATEGORY_META: Record<string, CategoryMeta> = {
  bakery: {
    label: "Panadería",
    icon: Croissant,
    image:
      "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop&auto=format",
  },
  restaurant: {
    label: "Restaurante",
    icon: Utensils,
    image:
      "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&h=300&fit=crop&auto=format",
  },
  cafe: {
    label: "Cafetería",
    icon: Coffee,
    image:
      "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop&auto=format",
  },
  market: {
    label: "Mercado",
    icon: ShoppingBasket,
    image:
      "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop&auto=format",
  },
  sushi: {
    label: "Sushi / Asiático",
    icon: Fish,
    image:
      "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400&h=300&fit=crop&auto=format",
  },
};

export function categoryMeta(category: string | null | undefined): CategoryMeta {
  if (category && CATEGORY_META[category.toLowerCase()]) {
    return CATEGORY_META[category.toLowerCase()];
  }
  return {
    label: category || DEFAULT_CATEGORY_META.label,
    icon: DEFAULT_CATEGORY_META.icon,
    image: DEFAULT_CATEGORY_META.image,
  };
}

export function categoryImage(category: string | null | undefined): string {
  return categoryMeta(category).image;
}

export function categoryIcon(category: string | null | undefined): LucideIcon {
  return categoryMeta(category).icon;
}

export function categoryLabel(category: string | null | undefined): string {
  return categoryMeta(category).label;
}

// ─── TAGS POR CATEGORÍA ───────────────────────────────────────────────────────

const CATEGORY_TAGS: Record<string, string[]> = {
  bakery: ["Pan", "Dulce", "Artesanal"],
  restaurant: ["Cocina", "Casero", "Gourmet"],
  cafe: ["Café", "Sándwich", "Postre"],
  market: ["Fresco", "Orgánico", "De temporada"],
  sushi: ["Sushi", "Fresco", "Japonés"],
};

const DEFAULT_TAGS = ["Rescate", "Sorpresa", "Fresco"];

export function categoryTags(category: string | null | undefined): string[] {
  if (category && CATEGORY_TAGS[category.toLowerCase()]) {
    return CATEGORY_TAGS[category.toLowerCase()];
  }
  return DEFAULT_TAGS;
}
