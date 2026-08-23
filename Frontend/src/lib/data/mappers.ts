import type {
  Bag,
  Business,
  Offer,
  Order,
  Reservation,
  Restaurant,
  Review,
  ReviewView,
} from "../types";
import {
  formatPickupRange,
  formatTime,
  haversineKm,
  parseWktPoint,
  timeAgo,
} from "../format";
import { categoryImage, categoryTags } from "../images";
import {
  cachedRating,
  getBusinessCached,
  getOfferCached,
} from "./cache";

const DEFAULT_IMAGE =
  "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop&auto=format";

// ─── OFERTA → BOLSA ──────────────────────────────────────────────────────────

export function offerToBag(
  offer: Offer,
  coords?: { lat: number; lng: number } | null,
): Bag {
  const business = offer.business ?? undefined;
  const id = offer.id ?? 0;
  const ratingInfo = cachedRating(offer.business_id);
  const distance = computeDistance(business, coords);

  return {
    id,
    restaurant: business?.name || `Comercio #${offer.business_id}`,
    restaurantId: offer.business_id,
    category: business?.category ?? "",
    type: offer.title,
    description: offer.description ?? "",
    image: business ? categoryImage(business.category) : DEFAULT_IMAGE,
    price: offer.discounted_price,
    originalValue: offer.original_price,
    rating: ratingInfo?.rating ?? 0,
    reviews: ratingInfo?.count ?? 0,
    distance,
    pickup: formatPickupRange(offer.pickup_start_time, offer.pickup_end_time),
    pickupEnd: offer.pickup_end_time,
    remaining: offer.quantity_available ?? 0,
    tags: categoryTags(business?.category),
    co2Saved: offer.co2_avoided_per_unit ?? 0,
    kgSaved:
      offer.kg_saved_per_unit ??
      +( (offer.co2_avoided_per_unit ?? 0) * 1.3 ).toFixed(1),
  };
}

function computeDistance(
  business: Business | undefined,
  coords?: { lat: number; lng: number } | null,
): string | null {
  if (coords) {
    const point = parseWktPoint(business?.location);
    if (point) {
      const km = haversineKm(coords, point);
      return `${km.toFixed(1)} km`;
    }
  }
  return business?.address ?? null;
}

// ─── BOLSAS → COMERCIOS ──────────────────────────────────────────────────────

export function groupBagsToRestaurants(bags: Bag[]): Restaurant[] {
  const map = new Map<number, Restaurant>();
  for (const bag of bags) {
    const existing = map.get(bag.restaurantId);
    if (existing) {
      existing.bags.push(bag);
      if (existing.distance == null && bag.distance != null) {
        existing.distance = bag.distance;
      }
      continue;
    }
    const ratingInfo = cachedRating(bag.restaurantId);
    map.set(bag.restaurantId, {
      id: bag.restaurantId,
      name: bag.restaurant,
      category: bag.category,
      image: bag.image,
      address: null,
      rating: ratingInfo?.rating ?? bag.rating,
      reviews: ratingInfo?.count ?? bag.reviews,
      distance: bag.distance,
      bags: [bag],
    });
  }
  return Array.from(map.values());
}

// ─── RESERVA → PEDIDO ────────────────────────────────────────────────────────

export async function reservationToOrder(
  reservation: Reservation,
): Promise<Order> {
  const offer = await getOfferCached(reservation.offer_id);
  const business = offer
    ? await getBusinessCached(offer.business_id)
    : null;

  const restaurant = business?.name
    ? business.name
    : offer
      ? `Comercio #${offer.business_id}`
      : "Comercio eliminado";
  const image = business ? categoryImage(business.category) : DEFAULT_IMAGE;

  return {
    id: reservation.id ?? 0,
    code: `ORD-${reservation.id ?? 0}`,
    restaurant,
    restaurantId: offer?.business_id ?? 0,
    image,
    date: timeAgo(reservation.created_at),
    pickup: formatPickupRange(
      offer?.pickup_start_time,
      offer?.pickup_end_time,
    ),
    status: reservation.status,
    price: reservation.total_price ?? 0,
    originalValue: offer?.original_price ?? reservation.total_price ?? 0,
    donated: reservation.transaction_fee ?? 0,
    quantity: reservation.quantity ?? 1,
    offerId: reservation.offer_id,
    active: reservation.status === "pending" || reservation.status === "paid",
    co2Saved:
      (offer?.co2_avoided_per_unit ?? 0) * (reservation.quantity ?? 1),
  };
}

// ─── REVIEWS (BACKEND) → VISTA ───────────────────────────────────────────────

const FIRST_NAMES = ["Ana", "Carlos", "María", "Diego", "Sofía", "Valentina"];

/** Alias amigable para un user_id (UUID) en la vista del comerciante. */
export function clientAlias(userId: string): string {
  const initials = userId.slice(0, 2).toUpperCase();
  return `${FIRST_NAMES[Math.abs(hashCode(userId)) % FIRST_NAMES.length]} ${initials}.`;
}

export function reviewToView(review: Review): ReviewView {
  const initials = review.user_id.slice(0, 2).toUpperCase();
  const name =
    FIRST_NAMES[Math.abs(hashCode(review.user_id)) % FIRST_NAMES.length] +
    ` ${initials}.`;
  return {
    user: name,
    rating: review.rating,
    text: review.comment ?? "",
    date: timeAgo(review.created_at),
  };
}

function hashCode(str: string): number {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (h << 5) - h + str.charCodeAt(i);
    h |= 0;
  }
  return h;
}

// ─── POSICIONES DEL MAPA ESTILIZADO (deterministas por id) ───────────────────

export function mapPositionForId(id: number): { x: number; y: number } {
  const x = 20 + ((id * 37) % 60);
  const y = 20 + ((id * 53) % 60);
  return { x, y };
}

// ─── HELPERS DE HORARIO PARA EL PANEL COMERCIANTE ────────────────────────────

/** "HH:mm" + fecha de hoy → ISO para enviar al backend. */
export function todayIsoAt(time: string): string {
  const [h, m] = time.split(":").map((n) => parseInt(n, 10));
  const d = new Date();
  d.setHours(h || 0, m || 0, 0, 0);
  return d.toISOString();
}

export { formatTime };
