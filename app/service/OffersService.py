from typing import List, Optional
from datetime import datetime
from app.entity.OffersEntity import OffersEntity
from app.repository.OffersRepository import OffersRepository

class OffersService:
    def __init__(self):
        self.offers_repository = OffersRepository()

    def get_all_offers(self) -> List[OffersEntity]:
        return self.offers_repository.get_all()

    def get_offer_by_id(self, offer_id: int) -> Optional[OffersEntity]:
        return self.offers_repository.get_by_id(offer_id)

    def create_offer(
        self,
        business_id: int,
        title: str,
        original_price: float,
        discounted_price: float,
        pickup_start_time: datetime,
        pickup_end_time: datetime,
        description: Optional[str] = None,
        quantity_available: int = 1,
        status: str = "active",
        kg_saved_per_unit: Optional[float] = None,
        co2_avoided_per_unit: Optional[float] = None
    ) -> OffersEntity:
        # El backend calcula y asocia los kg salvados y el CO2 evitado por unidad si no se envían
        if kg_saved_per_unit is None:
            kg_saved_per_unit = round(original_price / 5000.0, 2) if original_price > 0 else 1.0

        if co2_avoided_per_unit is None:
            co2_avoided_per_unit = round(kg_saved_per_unit * 2.5, 2)

        offer = OffersEntity(
            business_id=business_id,
            title=title,
            description=description,
            original_price=original_price,
            discounted_price=discounted_price,
            quantity_available=quantity_available,
            pickup_start_time=pickup_start_time,
            pickup_end_time=pickup_end_time,
            status=status,
            kg_saved_per_unit=kg_saved_per_unit,
            co2_avoided_per_unit=co2_avoided_per_unit
        )
        return self.offers_repository.create(offer)

    def update_offer(self, offer_id: int, data: dict) -> Optional[OffersEntity]:
        return self.offers_repository.update(offer_id, data, "id")

    def delete_offer(self, offer_id: int) -> bool:
        return self.offers_repository.delete(offer_id, "id")
    # Obtener las ofertas de un negocio
    def offers_by_business(self, business_id: int) -> List[OffersEntity]:
        return self.offers_repository.get_offers_by_business(business_id)
    # Obtener las ofertas activas de un negocio
    def get_active_offers_by_business(self, business_id: int) -> List[OffersEntity]:
        return self.offers_repository.get_active_offers_by_business(business_id)