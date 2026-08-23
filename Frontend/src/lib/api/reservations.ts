import { api } from "./client";
import type { Reservation } from "../types";

export interface CreateReservationPayload {
  offer_id: number;
  quantity: number;
  payment_method?: string | null;
  transaction_fee?: number | null;
}

export function createReservationApi(payload: CreateReservationPayload) {
  return api<Reservation>("/reservations/create", {
    method: "POST",
    body: payload,
  });
}

export function getMyReservationsApi() {
  return api<Reservation[]>("/reservations/my-reservations");
}

export function getAllReservationsApi() {
  return api<Reservation[]>("/reservations/get_all");
}

export function payReservationApi(id: number) {
  return api<Reservation>(`/reservations/pay/${id}`, { method: "POST" });
}

export function cancelReservationApi(id: number) {
  return api<Reservation>(`/reservations/cancel/${id}`, { method: "POST" });
}

export function updateReservationApi(id: number, data: Record<string, unknown>) {
  return api<Reservation>(`/reservations/update/${id}`, {
    method: "PATCH",
    body: data,
  });
}
