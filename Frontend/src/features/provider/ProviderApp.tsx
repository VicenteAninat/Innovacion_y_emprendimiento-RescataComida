import { useCallback, useEffect, useState } from "react";
import { Store } from "lucide-react";
import type { Business, Offer, Reservation } from "../../lib/types";
import { useAuth } from "../auth/AuthContext";
import { getBusinessCached } from "../../lib/data/cache";
import { getOffersByBusinessApi } from "../../lib/api/offers";
import { getAllReservationsApi } from "../../lib/api/reservations";
import ProviderBottomNav from "./ProviderBottomNav";
import ProviderDashboard from "./ProviderDashboard";
import ProviderBagsScreen from "./ProviderBagsScreen";
import ProviderOrdersScreen from "./ProviderOrdersScreen";
import ProviderStoreScreen from "./ProviderStoreScreen";
import MerchantPanel from "./MerchantPanel";
import type { ProviderTab } from "../../lib/types";

export default function ProviderApp({
  onSwitchToConsumer,
  onLogout,
}: {
  onSwitchToConsumer: () => void;
  onLogout: () => void;
}) {
  const { user } = useAuth();
  const businessId = user?.business_id ?? null;

  const [activeTab, setActiveTab] = useState<ProviderTab>("dashboard");
  const [business, setBusiness] = useState<Business | null>(null);
  const [offers, setOffers] = useState<Offer[]>([]);
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showPublish, setShowPublish] = useState(false);
  const [editOffer, setEditOffer] = useState<Offer | null>(null);

  const load = useCallback(async () => {
    if (businessId == null) {
      setLoading(false);
      setError(
        "Tu cuenta no está vinculada a un comercio. Pide a un administrador que asocie tu cuenta (business_id).",
      );
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const b = await getBusinessCached(businessId);
      const offs = await getOffersByBusinessApi(businessId);
      const resvs = await getAllReservationsApi();
      setBusiness(b);
      setOffers(offs);
      const offerIds = new Set(offs.map((o) => o.id ?? 0));
      setReservations(resvs.filter((r) => offerIds.has(r.offer_id)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar datos.");
    } finally {
      setLoading(false);
    }
  }, [businessId]);

  useEffect(() => {
    load();
  }, [load]);

  const handleSaved = () => {
    setEditOffer(null);
    load();
  };

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-1 overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="w-8 h-8 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
          </div>
        )}

        {!loading && (error || !business) && (
          <div className="flex flex-col items-center justify-center py-20 px-8">
            <Store size={36} className="text-muted-foreground mb-3" />
            <p className="text-sm text-muted-foreground text-center leading-relaxed mb-5">
              {error ?? "No se encontró el comercio asociado a tu cuenta."}
            </p>
            <button
              onClick={onSwitchToConsumer}
              className="h-11 px-6 rounded-2xl bg-primary text-white text-sm font-bold"
            >
              Volver al modo consumidor
            </button>
          </div>
        )}

        {!loading && business && (
          <>
            {activeTab === "dashboard" && (
              <ProviderDashboard
                business={business}
                offers={offers}
                reservations={reservations}
                onPublish={() => setShowPublish(true)}
              />
            )}
            {activeTab === "bags" && (
              <ProviderBagsScreen
                business={business}
                offers={offers}
                onPublish={() => setShowPublish(true)}
                onEdit={(offer) => setEditOffer(offer)}
                onReload={load}
              />
            )}
            {activeTab === "orders" && (
              <ProviderOrdersScreen
                reservations={reservations}
                offers={offers}
                onReload={load}
              />
            )}
            {activeTab === "store" && (
              <ProviderStoreScreen
                business={business}
                onSwitchToConsumer={onSwitchToConsumer}
                onLogout={onLogout}
              />
            )}
          </>
        )}
      </div>
      <ProviderBottomNav activeTab={activeTab} onChange={setActiveTab} />

      {business && (showPublish || editOffer) && (
        <MerchantPanel
          mode={editOffer ? "edit" : "create"}
          business={business}
          initial={editOffer}
          onClose={() => {
            setShowPublish(false);
            setEditOffer(null);
          }}
          onSaved={handleSaved}
        />
      )}
    </div>
  );
}
