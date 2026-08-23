import { api } from "./client";
import type { Review } from "../types";

export function createReviewApi(payload: {
  reservation_id: number;
  rating: number;
  comment?: string | null;
}) {
  return api<Review>("/reviews/create", { method: "POST", body: payload });
}

export function getBusinessReviewsApi(businessId: number) {
  return api<Review[]>(`/reviews/business/${businessId}`);
}
