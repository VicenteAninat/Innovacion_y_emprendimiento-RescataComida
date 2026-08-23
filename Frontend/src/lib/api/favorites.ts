import { api } from "./client";
import type { Business } from "../types";

export function addFavoriteApi(businessId: number) {
  return api<unknown>(`/favorites/add/${businessId}`, { method: "POST" });
}

export function removeFavoriteApi(businessId: number) {
  return api<boolean>(`/favorites/remove/${businessId}`, { method: "DELETE" });
}

export function getMyFavoritesApi() {
  return api<Business[]>("/favorites/my-favorites");
}
