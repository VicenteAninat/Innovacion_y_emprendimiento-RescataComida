import { useState } from "react";
import { ArrowLeft, Check, Clock } from "lucide-react";
import type { Bag } from "../../../lib/types";
import { fmt } from "../../../lib/format";
import {
  createReservationApi,
  payReservationApi,
} from "../../../lib/api/reservations";

export default function PaymentSheet({
  bag,
  onBack,
  onConfirmed,
}: {
  bag: Bag;
  onBack: () => void;
  onConfirmed: () => void;
}) {
  const [donate, setDonate] = useState(false);
  const [cardNumber, setCardNumber] = useState("");
  const [cardExpiry, setCardExpiry] = useState("");
  const [cardCvc, setCardCvc] = useState("");
  const [processing, setProcessing] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const donationAmount = Math.round((bag.price * 0.1) / 10) * 10;
  const total = donate ? bag.price + donationAmount : bag.price;

  const formatCard = (v: string) =>
    v.replace(/\D/g, "").slice(0, 16).replace(/(\d{4})(?=\d)/g, "$1 ");
  const formatExpiry = (v: string) =>
    v.replace(/\D/g, "").slice(0, 4).replace(/(\d{2})(?=\d)/, "$1/");

  const handleConfirm = async () => {
    setError(null);
    setProcessing(true);
    try {
      // 1. Crear la reserva en el backend (el trigger descuenta stock)
      const reservation = await createReservationApi({
        offer_id: bag.id,
        quantity: 1,
        payment_method: "card",
        transaction_fee: donate ? donationAmount : null,
      });
      // 2. Registrar el pago (ventana de 15 min)
      if (reservation.id != null) {
        await payReservationApi(reservation.id);
      }
      setProcessing(false);
      setSuccess(true);
      setTimeout(onConfirmed, 1400);
    } catch (err) {
      setProcessing(false);
      setError(
        err instanceof Error
          ? err.message
          : "No se pudo completar la reserva.",
      );
    }
  };

  return (
    <div className="absolute inset-0 flex flex-col" style={{ zIndex: 60 }}>
      <div className="absolute inset-0 bg-black/60" onClick={onBack} />
      <div className="absolute bottom-0 left-0 right-0 bg-background rounded-t-3xl overflow-hidden flex flex-col max-h-[94%]">
        {/* Header */}
        <div className="flex items-center gap-3 p-5 border-b border-border shrink-0">
          <button
            onClick={onBack}
            className="w-9 h-9 rounded-full bg-muted flex items-center justify-center"
          >
            <ArrowLeft size={18} className="text-foreground" />
          </button>
          <h2
            className="font-bold text-base text-foreground"
            style={{ fontFamily: "'Righteous', sans-serif" }}
          >
            Pago seguro
          </h2>
          <div className="ml-auto flex items-center gap-1 bg-accent/10 rounded-full px-2 py-0.5">
            <div className="w-1.5 h-1.5 rounded-full bg-accent" />
            <span className="text-[10px] font-bold text-accent">SSL</span>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-4 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {error && (
            <div className="bg-primary/10 border border-primary/20 rounded-2xl p-3.5">
              <p className="text-xs text-foreground leading-relaxed">{error}</p>
            </div>
          )}

          {/* Order summary */}
          <div className="bg-muted rounded-2xl p-4">
            <p className="text-[10px] text-muted-foreground mb-2 font-bold uppercase tracking-widest">
              Resumen
            </p>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl overflow-hidden bg-card shrink-0">
                <img
                  src={bag.image}
                  alt={bag.restaurant}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-bold text-sm text-foreground truncate">
                  {bag.restaurant}
                </p>
                <p className="text-xs text-muted-foreground truncate">
                  {bag.type}
                </p>
                <div className="flex items-center gap-1 mt-0.5">
                  <Clock size={9} className="text-muted-foreground" />
                  <span className="text-[9px] text-muted-foreground">
                    Retiro: {bag.pickup}
                  </span>
                </div>
              </div>
              <p className="font-black text-primary shrink-0">
                {fmt(bag.price)}
              </p>
            </div>
          </div>

          {/* Donation toggle */}
          <button
            onClick={() => setDonate(!donate)}
            className={`w-full rounded-2xl p-4 border-2 text-left transition-all ${
              donate ? "border-accent bg-accent/10" : "border-border bg-card"
            }`}
          >
            <div className="flex items-start gap-3">
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center mt-0.5 shrink-0 transition-all ${
                  donate ? "bg-accent" : "bg-muted"
                }`}
              >
                {donate && <Check size={13} className="text-white" />}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <p className="font-bold text-sm text-foreground">
                    Donar al Banco de Alimentos
                  </p>
                  <span className="bg-accent/20 text-accent text-[9px] font-black px-1.5 py-0.5 rounded-full">
                    Deducible de impuesto
                  </span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Agrega {fmt(donationAmount)} para ayudar a familias
                  vulnerables. Certificado tributario según Ley 20.241.
                </p>
              </div>
            </div>
          </button>

          {/* Card input */}
          <div className="space-y-3">
            <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
              Datos de la tarjeta
            </p>
            <div className="bg-card rounded-2xl border border-border p-4 space-y-3">
              <div>
                <p className="text-[10px] text-muted-foreground mb-1">
                  Número de tarjeta
                </p>
                <input
                  type="text"
                  inputMode="numeric"
                  placeholder="1234 5678 9012 3456"
                  value={cardNumber}
                  onChange={(e) => setCardNumber(formatCard(e.target.value))}
                  className="w-full bg-transparent text-sm font-mono outline-none text-foreground placeholder:text-muted-foreground"
                />
              </div>
              <div className="border-t border-border" />
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-[10px] text-muted-foreground mb-1">
                    Vencimiento
                  </p>
                  <input
                    type="text"
                    inputMode="numeric"
                    placeholder="MM/AA"
                    value={cardExpiry}
                    onChange={(e) => setCardExpiry(formatExpiry(e.target.value))}
                    className="w-full bg-transparent text-sm font-mono outline-none text-foreground placeholder:text-muted-foreground"
                  />
                </div>
                <div>
                  <p className="text-[10px] text-muted-foreground mb-1">CVC</p>
                  <input
                    type="text"
                    inputMode="numeric"
                    placeholder="123"
                    value={cardCvc}
                    onChange={(e) =>
                      setCardCvc(e.target.value.replace(/\D/g, "").slice(0, 3))
                    }
                    className="w-full bg-transparent text-sm font-mono outline-none text-foreground placeholder:text-muted-foreground"
                  />
                </div>
              </div>
            </div>

            {/* Chilean payment methods */}
            <div className="flex items-center gap-2">
              <div className="flex-1 h-px bg-border" />
              <span className="text-[10px] text-muted-foreground px-1">
                o paga con
              </span>
              <div className="flex-1 h-px bg-border" />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button className="bg-card border border-border rounded-xl py-2.5 flex items-center justify-center">
                <span className="text-sm font-black text-[#1A73E8]">Web</span>
                <span className="text-sm font-black text-[#E94E34]">pay</span>
              </button>
              <button className="bg-card border border-border rounded-xl py-2.5 flex items-center justify-center">
                <span className="text-xs font-black text-[#009ee3]">
                  Mercado Pago
                </span>
              </button>
            </div>
          </div>

          {/* Total breakdown */}
          <div className="bg-muted rounded-2xl p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Bolsa sorpresa</span>
              <span className="font-semibold">{fmt(bag.price)}</span>
            </div>
            {donate && (
              <div className="flex justify-between text-sm">
                <span className="text-accent">Donación banco de alimentos</span>
                <span className="font-semibold text-accent">
                  {fmt(donationAmount)}
                </span>
              </div>
            )}
            <div className="border-t border-border pt-2 flex justify-between">
              <span className="font-bold text-foreground">Total a pagar</span>
              <span className="font-black text-lg text-primary">
                {fmt(total)}
              </span>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="px-5 pb-6 pt-3 border-t border-border shrink-0">
          <button
            onClick={handleConfirm}
            disabled={processing || success}
            className={`w-full h-14 rounded-2xl font-bold text-base transition-all flex items-center justify-center gap-2 ${
              success
                ? "bg-accent text-white"
                : "bg-primary text-white active:scale-[0.98]"
            }`}
          >
            {success ? (
              <>
                <Check size={18} />
                ¡Pago confirmado!
              </>
            ) : processing ? (
              <>
                <div className="w-4 h-4 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                Creando reserva...
              </>
            ) : (
              `Pagar ${fmt(total)}`
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
