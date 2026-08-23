import { api } from "./client";
import type { Business } from "../types";

export function getBusinessesApi() {
  return api<Business[]>("/businesses/get_all");
}

export function getBusinessApi(id: number) {
  return api<Business>(`/businesses/get/${id}`);
}
