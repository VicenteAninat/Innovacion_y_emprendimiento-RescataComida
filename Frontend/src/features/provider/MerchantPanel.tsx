import { useState } from "react";
import {
  ArrowLeft,
  Check,
  Coffee,
  Croissant,
  Fish,
  Leaf,
  ShoppingBasket,
  Utensils,
  X,
  type LucideIcon,
} from "lucide-react";
import type { Business, Offer } from "../../lib/types";
import { formatTime, todayIsoAt } from "../../lib/data/mappers";
import { createOfferApi, updateOfferApi } from "../../lib/api/offers";
import { categoryIcon, categoryLabel } from "../../lib/images";

const MERCHANT_CATEGORIES: { id: string; label: string; icon: LucideIcon }[] = [
  { id: "bakery", label: "Panadería", icon: Croissant },
  { id: "restaurant", label: "Restaurante", icon: Utensils },
  { id: "cafe", label: "Cafetería", icon: Coffee },
  { id: "market", label: "Mercado", icon: ShoppingBasket },
  { id: "sushi", label: "Sushi / Asiático", icon: Fish },
];

export default function MerchantPanel({
  mode,
  business,
  initial,
  onClose,
  onSaved,
}: {
  mode: "create" | "edit";
  business: Business;
  initial?: Offer | null;
  onClose: () => void;
  onSaved: () => void;
}) {
  const [step, setStep] = useState(0);
  const [published, setPublished] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState({
    category: business.category ?? "",
    name: initial?.title ?? "",
    price: initial ? String(initial.discounted_price) : "",
    originalPrice: initial ? String(initial.original_price) : "",
    quantity: initial ? String(initial.quantity_available) : "5",
    pickupStart: initial ? formatTime(initial.pickup_start_time) || "19:00" : "19:00",
    pickupEnd: initial ? formatTime(initial.pickup_end_time) || "21:00" : "21:00",
  });

  const update = (key: string, value: string) =>
    setData((d) => ({ ...d, [key]: value }));

  const pctOfOriginal =
    data.price && data.originalPrice
      ? Math.round(
          (parseInt(data.price) / parseInt(data.originalPrice)) * 100,
        )
      : null;

  const handlePublish = async () => {
    setError(null);
    setSubmitting(true);
    try {
      const payload = {
        title: data.name,
        original_price: parseInt(data.originalPrice),
        discounted_price: parseInt(data.price),
        quantity_available: parseInt(data.quantity),
        pickup_start_time: todayIsoAt(data.pickupStart),
        pickup_end_time: todayIsoAt(data.pickupEnd),
        status: "active",
      };
      if (mode === "edit" && initial?.id != null) {
        await updateOfferApi(initial.id, payload);
      } else {
        await createOfferApi({
          business_id: business.id ?? 0,
          ...payload,
        });
      }
      setSubmitting(false);
      setPublished(true);
      setTimeout(() => {
        onSaved();
        onClose();
      }, 1600);
    } catch (err) {
      setSubmitting(false);
      setError(err instanceof Error ? err.message : "No se pudo publicar.");
    }
  };

  const canContinue = [
    mode === "edit"
      ? data.name !== ""
      : data.category !== "" && data.name !== "",
    data.price !== "" && data.originalPrice !== "",
    true,
  ][step];

  const CategoryIcon = categoryIcon(data.category);
  const categoryLabelFor = categoryLabel(data.category);

  return (
    <div
      className="absolute inset-0 bg-background flex flex-col"
      style={{ zIndex: 70 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-5 pt-5 pb-4 border-b border-border shrink-0">
        <div className="flex items-center gap-3">
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-full bg-muted flex items-center justify-center"
          >
            <X size={18} className="text-foreground" />
          </button>
          <h2
            className="font-bold text-base text-foreground"
            style={{ fontFamily: "'Righteous', sans-serif" }}
          >
            {mode === "edit" ? "Editar Bolsa Sorpresa" : "Publicar Bolsa Sorpresa"}
          </h2>
        </div>
        {/* Step indicators */}
        <div className="flex gap-1.5">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className={`h-1.5 rounded-full transition-all ${
                i < step
                  ? "bg-accent w-5"
                  : i === step
                    ? "bg-primary w-7"
                    : "bg-muted w-4"
              }`}
            />
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {error && (
          <div className="mb-4 bg-primary/10 border border-primary/20 rounded-2xl p-3.5">
            <p className="text-xs text-foreground leading-relaxed">{error}</p>
          </div>
        )}

        {/* Step 0: Category & name */}
        {step === 0 && (
          <div>
            <h3
              className="font-black text-2xl mb-1 text-foreground"
              style={{ fontFamily: "'Righteous', sans-serif" }}
            >
              ¿Qué tipo de bolsa?
            </h3>
            <p className="text-sm text-muted-foreground mb-5">
              {mode === "edit"
                ? `Categoría de tu comercio: ${categoryLabelFor}`
                : "Selecciona la categoría de tu comercio"}
            </p>
            {mode === "create" && (
              <div className="grid grid-cols-2 gap-3 mb-5">
                {MERCHANT_CATEGORIES.map((cat) => {
                  const Icon = cat.icon;
                  return (
                    <button
                      key={cat.id}
                      onClick={() => update("category", cat.id)}
                      className={`flex flex-col items-center gap-2 p-4 rounded-2xl border-2 transition-all ${
                        data.category === cat.id
                          ? "border-primary bg-primary/10"
                          : "border-border bg-card"
                      }`}
                    >
                      <Icon size={26} className="text-foreground" />
                      <span className="text-xs font-bold text-foreground">
                        {cat.label}
                      </span>
                    </button>
                  );
                })}
              </div>
            )}
            <div>
              <p className="text-xs font-bold text-muted-foreground mb-2">
                Nombre de tu bolsa
              </p>
              <input
                type="text"
                placeholder="Ej: Bolsa Sorpresa de Repostería"
                value={data.name}
                onChange={(e) => update("name", e.target.value)}
                className="w-full bg-card border border-border rounded-2xl px-4 h-12 text-sm outline-none text-foreground placeholder:text-muted-foreground"
              />
            </div>
          </div>
        )}

        {/* Step 1: Price & quantity */}
        {step === 1 && (
          <div>
            <h3
              className="font-black text-2xl mb-1 text-foreground"
              style={{ fontFamily: "'Righteous', sans-serif" }}
            >
              Precio y cantidad
            </h3>
            <p className="text-sm text-muted-foreground mb-5">
              El precio de venta debe ser 30–50% del valor original
            </p>
            <div className="space-y-4">
              <div>
                <p className="text-xs font-bold text-muted-foreground mb-2">
                  Valor original (CLP)
                </p>
                <div className="flex items-center bg-card border border-border rounded-2xl px-4 h-12 gap-2">
                  <span className="font-black text-muted-foreground text-lg">
                    $
                  </span>
                  <input
                    type="number"
                    placeholder="10000"
                    value={data.originalPrice}
                    onChange={(e) => update("originalPrice", e.target.value)}
                    className="flex-1 bg-transparent text-sm outline-none text-foreground"
                  />
                </div>
              </div>
              <div>
                <p className="text-xs font-bold text-muted-foreground mb-2">
                  Precio de venta (CLP)
                </p>
                <div className="flex items-center bg-card border border-border rounded-2xl px-4 h-12 gap-2">
                  <span className="font-black text-muted-foreground text-lg">
                    $
                  </span>
                  <input
                    type="number"
                    placeholder="3990"
                    value={data.price}
                    onChange={(e) => update("price", e.target.value)}
                    className="flex-1 bg-transparent text-sm outline-none text-foreground"
                  />
                </div>
                {pctOfOriginal !== null && (
                  <p
                    className={`text-xs mt-1.5 font-bold ${
                      pctOfOriginal <= 50 ? "text-accent" : "text-primary"
                    }`}
                  >
                    {pctOfOriginal}% del valor original
                    {pctOfOriginal <= 50
                      ? " Cumple el requisito"
                      : " — intenta reducir el precio"}
                  </p>
                )}
              </div>
              <div>
                <p className="text-xs font-bold text-muted-foreground mb-3">
                  Bolsas disponibles
                </p>
                <div className="flex items-center gap-5">
                  <button
                    onClick={() =>
                      update(
                        "quantity",
                        String(Math.max(1, parseInt(data.quantity) - 1)),
                      )
                    }
                    className="w-12 h-12 rounded-full bg-muted flex items-center justify-center text-2xl font-bold text-foreground"
                  >
                    −
                  </button>
                  <span className="text-3xl font-black text-foreground w-8 text-center">
                    {data.quantity}
                  </span>
                  <button
                    onClick={() =>
                      update("quantity", String(parseInt(data.quantity) + 1))
                    }
                    className="w-12 h-12 rounded-full bg-muted flex items-center justify-center text-2xl font-bold text-foreground"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Pickup time & preview */}
        {step === 2 && (
          <div>
            <h3
              className="font-black text-2xl mb-1 text-foreground"
              style={{ fontFamily: "'Righteous', sans-serif" }}
            >
              Ventana de retiro
            </h3>
            <p className="text-sm text-muted-foreground mb-5">
              Define cuándo pueden retirar los clientes
            </p>
            <div className="grid grid-cols-2 gap-3 mb-5">
              <div>
                <p className="text-xs font-bold text-muted-foreground mb-2">
                  Hora inicio
                </p>
                <input
                  type="time"
                  value={data.pickupStart}
                  onChange={(e) => update("pickupStart", e.target.value)}
                  className="w-full bg-card border border-border rounded-2xl px-4 h-12 text-sm outline-none text-foreground"
                />
              </div>
              <div>
                <p className="text-xs font-bold text-muted-foreground mb-2">
                  Hora fin
                </p>
                <input
                  type="time"
                  value={data.pickupEnd}
                  onChange={(e) => update("pickupEnd", e.target.value)}
                  className="w-full bg-card border border-border rounded-2xl px-4 h-12 text-sm outline-none text-foreground"
                />
              </div>
            </div>

            {/* Preview card */}
            <div className="bg-muted rounded-2xl p-4 mb-4">
              <p className="text-[10px] text-muted-foreground font-bold uppercase tracking-widest mb-3">
                Vista previa de tu bolsa
              </p>
              <div className="flex items-center gap-3">
                <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center shrink-0">
                  <CategoryIcon size={24} className="text-foreground" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-bold text-sm text-foreground truncate">
                    {data.name || "Nombre de tu bolsa"}
                  </p>
                  <p className="text-[10px] text-muted-foreground">
                    {data.pickupStart} – {data.pickupEnd} · {data.quantity} uds.
                  </p>
                  <div className="flex items-baseline gap-1.5 mt-0.5">
                    <span className="text-primary font-black">
                      ${parseInt(data.price || "0").toLocaleString("es-CL")}
                    </span>
                    <span className="text-muted-foreground text-[9px] line-through">
                      $
                      {parseInt(data.originalPrice || "0").toLocaleString(
                        "es-CL",
                      )}
                    </span>
                    {pctOfOriginal !== null && (
                      <span className="text-[9px] font-bold bg-secondary rounded-full px-1.5 py-0.5">
                        -{100 - pctOfOriginal}%
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Environmental estimate */}
            <div className="bg-accent/10 border border-accent/20 rounded-2xl p-3.5">
              <div className="flex items-center gap-2 mb-1">
                <Leaf size={14} className="text-accent shrink-0" />
                <p className="text-xs font-bold text-foreground">
                  Impacto estimado al publicar {data.quantity} bolsa(s)
                </p>
              </div>
              <p className="text-[10px] text-muted-foreground ml-5">
                ≈ {(parseInt(data.quantity) * 0.9).toFixed(1)} kg CO₂ evitado ·
                ≈ {(parseInt(data.quantity) * 1.2).toFixed(1)} kg de alimento
                rescatado
              </p>
            </div>
          </div>
        )}
      </div>

      {/* CTA */}
      <div className="px-5 pb-6 pt-3 border-t border-border shrink-0">
        <div className="flex gap-3">
          {step > 0 && (
            <button
              onClick={() => setStep((s) => s - 1)}
              className="w-12 h-14 rounded-2xl bg-muted flex items-center justify-center shrink-0"
            >
              <ArrowLeft size={18} className="text-foreground" />
            </button>
          )}
          <button
            onClick={() => {
              if (step < 2) setStep((s) => s + 1);
              else handlePublish();
            }}
            disabled={!canContinue || published || submitting}
            className={`flex-1 h-14 rounded-2xl font-bold text-base transition-all flex items-center justify-center gap-2 ${
              published
                ? "bg-accent text-white"
                : canContinue
                  ? "bg-primary text-white active:scale-[0.98]"
                  : "bg-muted text-muted-foreground"
            }`}
          >
            {published ? (
              <>
                <Check size={18} />
                {mode === "edit" ? "¡Bolsa actualizada!" : "¡Bolsa publicada!"}
              </>
            ) : submitting ? (
              <>
                <div className="w-4 h-4 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                Guardando...
              </>
            ) : step < 2 ? (
              "Continuar →"
            ) : mode === "edit" ? (
              "Guardar cambios"
            ) : (
              "Publicar ahora"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
