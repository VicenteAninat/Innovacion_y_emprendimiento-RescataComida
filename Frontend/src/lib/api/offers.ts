import { api } from "./client";
import type { Offer } from "../types";

export interface CreateOfferPayload {
  business_id: number;
  title: string;
  description?: string | null;
  original_price: number;
  discounted_price: number;
  quantity_available?: number;
  pickup_start_time: string;
  pickup_end_time: string;
  status?: string;
  kg_saved_per_unit?: number | null;
  co2_avoided_per_unit?: number | null;
}

export function getActiveOffersApi(params?: {
  lat?: number;
  lng?: number;
  radius_km?: number;
  limit?: number;
  offset?: number;
}) {
  const q = new URLSearchParams();
  if (params?.lat != null) q.set("lat", String(params.lat));
  if (params?.lng != null) q.set("lng", String(params.lng));
  if (params?.radius_km != null) q.set("radius_km", String(params.radius_km));
  if (params?.limit != null) q.set("limit", String(params.limit));
  if (params?.offset != null) q.set("offset", String(params.offset));
  const qs = q.toString();
  return api<Offer[]>(`/offers/active${qs ? `?${qs}` : ""}`);
}

export function getOfferApi(id: number) {
  return api<Offer>(`/offers/get/${id}`);
}

export function getOffersByBusinessApi(businessId: number) {
  return api<Offer[]>(`/offers/business/${businessId}`);
}

export function createOfferApi(payload: CreateOfferPayload) {
  return api<Offer>("/offers/create", { method: "POST", body: payload });
}

export function updateOfferApi(id: number, data: Record<string, unknown>) {
  return api<Offer>(`/offers/update/${id}`, { method: "PATCH", body: data });
}

export function deleteOfferApi(id: number) {
  return api<boolean>(`/offers/delete/${id}`, { method: "DELETE" });
}
