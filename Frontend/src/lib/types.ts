// ─── TIPOS DEL BACKEND (FastAPI / Supabase) ─────────────────────────────────

export type UserRole = "customer" | "worker" | "admin";

export interface User {
  id: string;
  name?: string | null;
  email: string;
  phone?: string | null;
  role: UserRole;
  business_id?: number | null;
  created_at?: string | null;
}

export interface GeoLocation {
  type?: string;
  coordinates?: number[];
}

export interface Business {
  id?: number | null;
  rut?: string | null;
  name?: string | null;
  category?: string | null;
  address?: string | null;
  location?: string | null | GeoLocation;
  is_premium?: boolean;
  created_at?: string | null;
}

export interface Offer {
  id?: number | null;
  business_id: number;
  title: string;
  description?: string | null;
  original_price: number;
  discounted_price: number;
  quantity_available: number;
  pickup_start_time: string;
  pickup_end_time: string;
  status: string;
  kg_saved_per_unit?: number | null;
  co2_avoided_per_unit?: number | null;
  created_at?: string | null;
  business?: Business | null;
}

export interface Reservation {
  id?: number | null;
  user_id: string;
  offer_id: number;
  quantity: number;
  total_price: number;
  status: string;
  payment_method?: string | null;
  transaction_fee?: number | null;
  created_at?: string | null;
  user?: User | null;
}

export interface Review {
  id?: number | null;
  user_id: string;
  business_id: number;
  reservation_id: number;
  rating: number;
  comment?: string | null;
  created_at?: string | null;
}

// ─── MODELOS DE VISTA (UI) ───────────────────────────────────────────────────

export type Tab = "home" | "explore" | "orders" | "profile";
export type ProviderTab = "dashboard" | "bags" | "orders" | "store";

/** Oferta del backend mapeada al modelo de "Bolsa Sorpresa" de la UI. */
export interface Bag {
  id: number;
  restaurant: string;
  restaurantId: number;
  category: string;
  type: string;
  description: string;
  image: string;
  price: number;
  originalValue: number;
  rating: number;
  reviews: number;
  distance: string | null;
  pickup: string;
  pickupEnd: string;
  remaining: number;
  tags: string[];
  co2Saved: number;
  kgSaved: number;
}

/** Agrupación de bolsas por comercio. */
export interface Restaurant {
  id: number;
  name: string;
  category: string;
  image: string;
  address: string | null;
  rating: number;
  reviews: number;
  distance: string | null;
  bags: Bag[];
}

/** Reserva del backend mapeada al modelo de pedido de la UI. */
export interface Order {
  id: number;
  code: string;
  restaurant: string;
  restaurantId: number;
  image: string;
  date: string;
  pickup: string;
  status: string;
  price: number;
  originalValue: number;
  donated: number;
  quantity: number;
  offerId: number;
  active: boolean;
  co2Saved: number;
}

export interface ReviewView {
  user: string;
  rating: number;
  text: string;
  date: string;
}
