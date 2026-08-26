import { useCallback, useEffect, useState } from "react";
import { Frown } from "lucide-react";
import type { Bag, Order, Restaurant, Tab } from "../../lib/types";
import { useAuth } from "../auth/AuthContext";
import { getActiveOffersApi } from "../../lib/api/offers";
import { getMyFavoritesApi, addFavoriteApi, removeFavoriteApi } from "../../lib/api/favorites";
import {
  getBusinessCached,
  getBusinessReviewsCached,
  getOfferCached,
} from "../../lib/data/cache";
import { offerToBag } from "../../lib/data/mappers";
import { requestUserLocation } from "../../lib/format";
import BottomNav from "../shared/BottomNav";
import HomeScreen from "./screens/HomeScreen";
import ExploreScreen from "./screens/ExploreScreen";
import OrdersScreen from "./screens/OrdersScreen";
import ProfileScreen from "./screens/ProfileScreen";
import RestaurantDetailSheet from "./sheets/RestaurantDetailSheet";
import BagDetailSheet from "./sheets/BagDetailSheet";
import PaymentSheet from "./sheets/PaymentSheet";
import WriteReviewSheet from "./sheets/WriteReviewSheet";

export default function ConsumerApp({
  onOpenMerchant,
  onLogout,
}: {
  onOpenMerchant: () => void;
  onLogout: () => void;
}) {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<Tab>("home");
  const [category, setCategory] = useState("all");

  const [bags, setBags] = useState<Bag[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [coords, setCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [favoriteIds, setFavoriteIds] = useState<Set<number>>(new Set());

  const [selectedBag, setSelectedBag] = useState<Bag | null>(null);
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [showPayment, setShowPayment] = useState(false);
  const [reviewOrder, setReviewOrder] = useState<Order | null>(null);
  const [ordersRefresh, setOrdersRefresh] = useState(0);

  // Geolocalización best-effort para calcular distancias
  useEffect(() => {
    requestUserLocation().then((pos) => setCoords(pos));
  }, []);

  const refreshFeed = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const offers = await getActiveOffersApi({ limit: 50 });
      let mapped = offers.map((o) => offerToBag(o, coords));
      setBags(mapped);
      // Pre-cargar reseñas para calcular rating en las tarjetas
      const businessIds = [...new Set(offers.map((o) => o.business_id))];
      for (const id of businessIds) {
        try {
          await getBusinessReviewsCached(id);
        } catch { /* ignorar */ }
      }
      mapped = offers.map((o) => offerToBag(o, coords));
      setBags(mapped);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar ofertas.");
    } finally {
      setLoading(false);
    }
  }, [coords]);

  useEffect(() => {
    refreshFeed();
  }, [refreshFeed]);

  // Favoritos (por comercio)
  const loadFavorites = useCallback(async () => {
    try {
      const favs = await getMyFavoritesApi();
      setFavoriteIds(
        new Set(
          favs
            .map((b) => b.id)
            .filter((id): id is number => id != null),
        ),
      );
    } catch {
      /* sin favoritos o error: ignorar */
    }
  }, []);

  useEffect(() => {
    loadFavorites();
  }, [loadFavorites]);

  const toggleFavorite = async (businessId: number) => {
    const wasFav = favoriteIds.has(businessId);
    setFavoriteIds((prev) => {
      const next = new Set(prev);
      if (wasFav) next.delete(businessId);
      else next.add(businessId);
      return next;
    });
    try {
      if (wasFav) await removeFavoriteApi(businessId);
      else await addFavoriteApi(businessId);
    } catch {
      // revertir cambio optimista
      setFavoriteIds((prev) => {
        const next = new Set(prev);
        if (wasFav) next.add(businessId);
        else next.delete(businessId);
        return next;
      });
    }
  };

  const handlePaymentConfirmed = () => {
    setShowPayment(false);
    setSelectedBag(null);
    setActiveTab("orders");
    setOrdersRefresh((n) => n + 1);
  };

  const handleRepeat = async (offerId: number) => {
    try {
      const offer = await getOfferCached(offerId);
      if (offer) {
        // /offers/get/{id} no anida el negocio: lo enriquecemos desde el caché
        const business = await getBusinessCached(offer.business_id);
        setSelectedBag(offerToBag({ ...offer, business }, coords));
      }
    } catch {
      /* oferta eliminada: ignorar */
    }
  };

  const handleReviewSubmitted = () => {
    setOrdersRefresh((n) => n + 1);
    refreshFeed();
  };

  return (
    <>
      <div className="h-full flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {loading && activeTab !== "orders" && (
            <div className="flex flex-col items-center justify-center py-20">
              <div className="w-8 h-8 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
              <p className="text-xs text-muted-foreground mt-3">
                Cargando bolsas disponibles...
              </p>
            </div>
          )}

          {!loading && error && (
            <div className="flex flex-col items-center justify-center py-20 px-8">
              <Frown size={36} className="text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground text-center leading-relaxed mb-5">
                {error}
              </p>
              <button
                onClick={refreshFeed}
                className="h-11 px-6 rounded-2xl bg-primary text-white text-sm font-bold"
              >
                Reintentar
              </button>
            </div>
          )}

          {!loading && !error && activeTab === "home" && (
            <HomeScreen
              bags={bags}
              category={category}
              setCategory={setCategory}
              onSelectBag={setSelectedBag}
              onSelectRestaurant={setSelectedRestaurant}
              favoriteIds={favoriteIds}
              onToggleFavorite={toggleFavorite}
            />
          )}
          {!loading && !error && activeTab === "explore" && (
            <ExploreScreen
              bags={bags}
              onSelectBag={setSelectedBag}
              favoriteIds={favoriteIds}
              onToggleFavorite={toggleFavorite}
            />
          )}
          {activeTab === "orders" && (
            <OrdersScreen
              onOpenReview={setReviewOrder}
              onRepeat={handleRepeat}
              refreshToken={ordersRefresh}
            />
          )}
          {activeTab === "profile" && user && (
            <ProfileScreen
              user={user}
              onOpenMerchant={onOpenMerchant}
              onLogout={onLogout}
            />
          )}
        </div>
        <BottomNav activeTab={activeTab} onChange={setActiveTab} />
      </div>

      {/* Restaurant detail */}
      {selectedRestaurant && !selectedBag && !showPayment && !reviewOrder && (
        <RestaurantDetailSheet
          restaurant={selectedRestaurant}
          onClose={() => setSelectedRestaurant(null)}
          onSelectBag={(bag) => {
            setSelectedBag(bag);
            setSelectedRestaurant(null);
          }}
        />
      )}

      {/* Bag detail */}
      {selectedBag && !showPayment && !reviewOrder && !selectedRestaurant && (
        <BagDetailSheet
          bag={selectedBag}
          onClose={() => setSelectedBag(null)}
          onOpenPayment={() => setShowPayment(true)}
          saved={favoriteIds.has(selectedBag.restaurantId)}
          onToggleSave={() => toggleFavorite(selectedBag.restaurantId)}
        />
      )}

      {/* Write review sheet */}
      {reviewOrder && (
        <WriteReviewSheet
          order={reviewOrder}
          onClose={() => setReviewOrder(null)}
          onSubmitted={handleReviewSubmitted}
        />
      )}

      {/* Payment sheet */}
      {selectedBag && showPayment && (
        <PaymentSheet
          bag={selectedBag}
          onBack={() => setShowPayment(false)}
          onConfirmed={handlePaymentConfirmed}
        />
      )}
    </>
  );
}
