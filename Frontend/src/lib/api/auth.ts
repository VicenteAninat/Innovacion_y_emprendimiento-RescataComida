import { api } from "./client";
import type { User } from "../types";

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: string;
  user: User;
}

export interface RegisterPayload {
  email: string;
  password: string;
  name?: string | null;
  phone?: string | null;
  role?: "customer" | "worker" | "admin";
  business_id?: number | null;
}

export function loginApi(email: string, password: string) {
  return api<LoginResponse>("/auth/login", {
    method: "POST",
    body: { email, password },
    auth: false,
  });
}

export function registerApi(payload: RegisterPayload) {
  return api<User>("/auth/register", {
    method: "POST",
    body: payload,
    auth: false,
  });
}

export function getProfileApi() {
  return api<User>("/auth/profile");
}

export function updateProfileApi(data: {
  name?: string;
  phone?: string;
}) {
  return api<User>("/auth/profile", { method: "PATCH", body: data });
}
