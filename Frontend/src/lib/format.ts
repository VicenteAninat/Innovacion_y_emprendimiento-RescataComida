// ─── HELPERS DE FORMATO ──────────────────────────────────────────────────────

export const fmt = (n: number) =>
  `$${n.toLocaleString("es-CL", { maximumFractionDigits: 0 })}`;

export const savingsPct = (price: number, original: number) =>
  original > 0 ? Math.round((1 - price / original) * 100) : 0;

const twoDigits = (n: number) => String(n).padStart(2, "0");

/** "2026-08-22T18:00:00" → "18:00 – 20:00" */
export function formatPickupRange(
  start: string | null | undefined,
  end: string | null | undefined,
): string {
  const parse = (iso: string | null | undefined) => {
    if (!iso) return null;
    const d = new Date(iso);
    if (isNaN(d.getTime())) return null;
    return d;
  };
  const s = parse(start);
  const e = parse(end);
  const time = (d: Date | null) =>
    d ? `${twoDigits(d.getHours())}:${twoDigits(d.getMinutes())}` : "--:--";
  return `${time(s)} – ${time(e)}`;
}

/** "2026-08-22T18:00:00" → "18:00" */
export function formatTime(iso: string | null | undefined): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d.getTime())) return "";
  return `${twoDigits(d.getHours())}:${twoDigits(d.getMinutes())}`;
}

/** ISO timestamp → "hace 5 min" / "ayer" / "17 Mayo, 17:45" */
export function timeAgo(iso: string | null | undefined): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d.getTime())) return "";
  const diffMs = Date.now() - d.getTime();
  const mins = Math.floor(diffMs / 60_000);
  if (mins < 1) return "ahora mismo";
  if (mins < 60) return `hace ${mins} min`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `hace ${hours} h`;
  const days = Math.floor(hours / 24);
  if (days === 1) return "ayer";
  const dateStr = d.toLocaleDateString("es-CL", {
    day: "numeric",
    month: "long",
  });
  const timeStr = `${twoDigits(d.getHours())}:${twoDigits(d.getMinutes())}`;
  return `${dateStr}, ${timeStr}`;
}

// ─── GEOLOCALIZACIÓN ─────────────────────────────────────────────────────────

/** Parsea WKT "POINT(lng lat)" o GeoJSON {type:"Point", coordinates:[lng,lat]} */
export function parseWktPoint(
  location:
    | string
    | null
    | undefined
    | { type?: string; coordinates?: number[] },
): { lat: number; lng: number } | null {
  if (!location) return null;
  if (typeof location === "object") {
    const coords = location.coordinates;
    if (Array.isArray(coords) && coords.length >= 2) {
      const [lng, lat] = coords;
      if (!isNaN(lng) && !isNaN(lat)) return { lat, lng };
    }
    return null;
  }
  const m = location.match(
    /point\s*\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)/i,
  );
  if (!m) return null;
  const lng = parseFloat(m[1]);
  const lat = parseFloat(m[2]);
  if (isNaN(lat) || isNaN(lng)) return null;
  return { lat, lng };
}

/** Distancia en km entre dos coordenadas (Haversine). */
export function haversineKm(
  a: { lat: number; lng: number },
  b: { lat: number; lng: number },
): number {
  const R = 6371;
  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const dLat = toRad(b.lat - a.lat);
  const dLng = toRad(b.lng - a.lng);
  const s =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}

/** Intenta obtener la ubicación del usuario (best-effort). */
export function requestUserLocation(): Promise<{
  lat: number;
  lng: number;
} | null> {
  return new Promise((resolve) => {
    if (!("geolocation" in navigator)) {
      resolve(null);
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) =>
        resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => resolve(null),
      { timeout: 4000, maximumAge: 5 * 60_000 },
    );
  });
}
