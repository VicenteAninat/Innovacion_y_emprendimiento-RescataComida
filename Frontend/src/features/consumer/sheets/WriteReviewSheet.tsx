import { useState } from "react";
import { ArrowLeft, Check, Star } from "lucide-react";
import type { Order } from "../../../lib/types";
import { createReviewApi } from "../../../lib/api/reviews";

export default function WriteReviewSheet({
  order,
  onClose,
  onSubmitted,
}: {
  order: Order;
  onClose: () => void;
  onSubmitted: () => void;
}) {
  const [rating, setRating] = useState(5);
  const [text, setText] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (text.trim().length < 10) return;
    setError(null);
    setSubmitting(true);
    try {
      await createReviewApi({
        reservation_id: order.id,
        rating,
        comment: text.trim(),
      });
      setSubmitting(false);
      setSuccess(true);
      setTimeout(() => {
        onSubmitted();
        onClose();
      }, 1200);
    } catch (err) {
      setSubmitting(false);
      setError(err instanceof Error ? err.message : "Error al publicar.");
    }
  };

  return (
    <div className="absolute inset-0 flex flex-col" style={{ zIndex: 65 }}>
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="absolute bottom-0 left-0 right-0 bg-background rounded-t-3xl overflow-hidden flex flex-col max-h-[90%]">
        {/* Header */}
        <div className="flex items-center gap-3 p-5 border-b border-border shrink-0">
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-full bg-muted flex items-center justify-center"
          >
            <ArrowLeft size={18} className="text-foreground" />
          </button>
          <h2
            className="font-bold text-base text-foreground"
            style={{ fontFamily: "'Righteous', sans-serif" }}
          >
            Escribir Reseña
          </h2>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {/* Restaurant info */}
          <div className="bg-muted rounded-2xl p-4 flex items-center gap-3">
            <div className="w-14 h-14 rounded-xl overflow-hidden bg-card shrink-0">
              <img
                src={order.image}
                alt={order.restaurant}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-bold text-sm text-foreground truncate">
                {order.restaurant}
              </p>
              <p className="text-xs text-muted-foreground truncate">
                Pedido {order.code}
              </p>
            </div>
          </div>

          {error && (
            <div className="bg-primary/10 border border-primary/20 rounded-2xl p-3.5">
              <p className="text-xs text-foreground leading-relaxed">{error}</p>
            </div>
          )}

          {/* Star rating */}
          <div>
            <p className="text-sm font-bold text-foreground mb-3">
              ¿Cómo fue tu experiencia?
            </p>
            <div className="flex items-center justify-center gap-3 py-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setRating(star)}
                  className="transition-transform active:scale-95"
                >
                  <Star
                    size={40}
                    className={
                      star <= rating
                        ? "fill-yellow-400 text-yellow-400"
                        : "text-muted-foreground"
                    }
                  />
                </button>
              ))}
            </div>
            <p className="text-center text-xs text-muted-foreground mt-2">
              {rating === 5
                ? "¡Excelente!"
                : rating === 4
                  ? "Muy bueno"
                  : rating === 3
                    ? "Bueno"
                    : rating === 2
                      ? "Regular"
                      : "Mejorable"}
            </p>
          </div>

          {/* Review text */}
          <div>
            <p className="text-sm font-bold text-foreground mb-2">
              Cuéntanos más (opcional)
            </p>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Comparte tu experiencia con esta bolsa sorpresa... ¿Qué venía? ¿Vale la pena?"
              className="w-full bg-card border border-border rounded-2xl p-4 text-sm text-foreground placeholder:text-muted-foreground outline-none resize-none h-32"
              maxLength={300}
            />
            <div className="flex items-center justify-between mt-2">
              <p className="text-[10px] text-muted-foreground">
                {text.length < 10 && text.length > 0
                  ? "Mínimo 10 caracteres"
                  : text.length >= 10
                    ? "Listo para publicar"
                    : ""}
              </p>
              <p className="text-[10px] text-muted-foreground">
                {text.length}/300
              </p>
            </div>
          </div>

          {/* Guidelines */}
          <div className="bg-accent/10 border border-accent/20 rounded-2xl p-3.5">
            <p className="text-xs font-bold text-foreground mb-1.5">
              Ayuda a la comunidad
            </p>
            <p className="text-[10px] text-muted-foreground leading-relaxed">
              Tu reseña ayuda a otros rescatadores a decidir mejor. Sé honesto,
              constructivo y respetuoso.
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="px-5 pb-6 pt-3 border-t border-border shrink-0">
          <button
            onClick={handleSubmit}
            disabled={submitting || success || text.trim().length < 10}
            className={`w-full h-14 rounded-2xl font-bold text-base transition-all flex items-center justify-center gap-2 ${
              success
                ? "bg-accent text-white"
                : text.trim().length >= 10
                  ? "bg-primary text-white active:scale-[0.98]"
                  : "bg-muted text-muted-foreground"
            }`}
          >
            {success ? (
              <>
                <Check size={18} />
                ¡Reseña publicada!
              </>
            ) : submitting ? (
              <>
                <div className="w-4 h-4 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                Publicando...
              </>
            ) : (
              "Publicar reseña"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
