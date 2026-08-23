import type { Business, Offer, Review } from "../types";
import { getBusinessApi } from "../api/businesses";
import { getOfferApi } from "../api/offers";
import { getBusinessReviewsApi } from "../api/reviews";

// Cachés en memoria por sesión: evitan N+1 repetido contra el backend.
const businessCache = new Map<number, Business>();
const offerCache = new Map<number, Offer>();
const reviewsCache = new Map<number, Review[]>();

export async function getBusinessCached(id: number): Promise<Business | null> {
  const cached = businessCache.get(id);
  if (cached) return cached;
  try {
    const business = await getBusinessApi(id);
    businessCache.set(id, business);
    return business;
  } catch {
    return null;
  }
}

export async function getOfferCached(id: number): Promise<Offer | null> {
  const cached = offerCache.get(id);
  if (cached) return cached;
  try {
    const offer = await getOfferApi(id);
    offerCache.set(id, offer);
    return offer;
  } catch {
    return null;
  }
}

export async function getBusinessReviewsCached(
  businessId: number,
): Promise<Review[]> {
  const cached = reviewsCache.get(businessId);
  if (cached) return cached;
  try {
    const reviews = await getBusinessReviewsApi(businessId);
    reviewsCache.set(businessId, reviews);
    return reviews;
  } catch {
    return [];
  }
}

/** Promedio de rating de un comercio a partir del caché (null si no hay datos). */
export function cachedRating(businessId: number): {
  rating: number;
  count: number;
} | null {
  const reviews = reviewsCache.get(businessId);
  if (!reviews || reviews.length === 0) return null;
  const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
  return {
    rating: Math.round((sum / reviews.length) * 10) / 10,
    count: reviews.length,
  };
}

/** True si ya existe una reseña para la reserva en el caché del comercio. */
export function reservationHasReview(
  businessId: number,
  reservationId: number,
): boolean {
  const reviews = reviewsCache.get(businessId);
  return (
    reviews?.some((r) => r.reservation_id === reservationId) ?? false
  );
}

export function clearCaches(): void {
  businessCache.clear();
  offerCache.clear();
  reviewsCache.clear();
}
