import { useMemo } from "react";
import { UtensilsCrossed } from "lucide-react";
import type { Bag, Restaurant } from "../../../lib/types";
import { groupBagsToRestaurants } from "../../../lib/data/mappers";
import SectionHeader from "../../shared/SectionHeader";
import SearchBar from "../../shared/SearchBar";
import TopBar from "../components/TopBar";
import FlashDeal from "../components/FlashDeal";
import CategoryPills, {
  buildCategoryOptions,
} from "../components/CategoryPills";
import RestaurantCard from "../components/RestaurantCard";
import BagCard from "../components/BagCard";

export default function HomeScreen({
  bags,
  category,
  setCategory,
  onSelectBag,
  onSelectRestaurant,
  favoriteIds,
  onToggleFavorite,
}: {
  bags: Bag[];
  category: string;
  setCategory: (c: string) => void;
  onSelectBag: (b: Bag) => void;
  onSelectRestaurant: (r: Restaurant) => void;
  favoriteIds: Set<number>;
  onToggleFavorite: (businessId: number) => void;
}) {
  const restaurants = useMemo(
    () => groupBagsToRestaurants(bags),
    [bags],
  );
  const categoryOptions = useMemo(() => buildCategoryOptions(bags), [bags]);

  const filteredRestaurants =
    category === "all"
      ? restaurants
      : restaurants.filter((r) => r.category === category);

  // Separate restaurants with multiple bags from single-bag restaurants
  const multiRestaurants = filteredRestaurants.filter(
    (r) => r.bags.length > 1,
  );
  const singleBagRestaurants = filteredRestaurants.filter(
    (r) => r.bags.length === 1,
  );

  // FlashDeal: bolsa con mayor % de descuento
  const flashDeal = useMemo(() => {
    if (bags.length === 0) return null;
    return [...bags].sort((a, b) => {
      const aPct = a.originalValue > 0 ? 1 - a.price / a.originalValue : 0;
      const bPct = b.originalValue > 0 ? 1 - b.price / b.originalValue : 0;
      return bPct - aPct;
    })[0];
  }, [bags]);

  return (
    <div className="pb-6">
      <TopBar />
      <div className="px-5 pb-4">
        <SearchBar />
      </div>
      {flashDeal && <FlashDeal bag={flashDeal} onSelect={onSelectBag} />}
      <SectionHeader title="Categorías" />
      <CategoryPills
        active={category}
        onChange={setCategory}
        options={categoryOptions}
      />

      {/* Restaurants with multiple bags */}
      {multiRestaurants.length > 0 && (
        <>
          <SectionHeader title="Comercios con varias opciones" action="Ver todo" />
          <div className="grid grid-cols-2 gap-3 px-5 mb-5">
            {multiRestaurants.map((restaurant) => (
              <RestaurantCard
                key={restaurant.id}
                restaurant={restaurant}
                onSelect={onSelectRestaurant}
              />
            ))}
          </div>
        </>
      )}

      {/* Single bag listings */}
      {singleBagRestaurants.length > 0 && (
        <>
          <SectionHeader title="Cerca de ti" action="Ver todo" />
          <div className="grid grid-cols-2 gap-3 px-5">
            {singleBagRestaurants.map((restaurant) => (
              <BagCard
                key={restaurant.bags[0].id}
                bag={restaurant.bags[0]}
                onSelect={onSelectBag}
                saved={favoriteIds.has(restaurant.bags[0].restaurantId)}
                onSave={() => onToggleFavorite(restaurant.bags[0].restaurantId)}
              />
            ))}
          </div>
        </>
      )}

      {filteredRestaurants.length === 0 && (
        <div className="flex flex-col items-center justify-center py-14 px-5">
          <UtensilsCrossed size={36} className="text-muted-foreground mb-3" />
          <p className="text-sm text-muted-foreground text-center">
            No hay bolsas disponibles en esta categoría ahora mismo.
          </p>
        </div>
      )}
    </div>
  );
}
