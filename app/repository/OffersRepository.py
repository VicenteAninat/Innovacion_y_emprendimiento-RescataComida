from typing import List
from app.entity.OffersEntity import OffersEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class OffersRepository(BaseRepository[OffersEntity]):
    def __init__(self):
        super().__init__(OffersEntity, "offers")

    def get_active_offers(self) -> List[OffersEntity]:
        # Lista ofertas con estado 'active' y cantidad disponible mayor a 0
        response = (
            supabase.table(self.table_name)
            .select("*, business(*)")
            .eq("status", "active")
            .gt("quantity_available", 0)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_offers_by_business(self, business_id: int) -> List[OffersEntity]:
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_favorite_businesses_offers_nearby(self, user_id: str, lat: float, lng: float, radius_km: float = 5.0) -> List[OffersEntity]:
        response = supabase.rpc(
            "get_favorite_businesses_offers_nearby",
            {
                "client_user_id": user_id,
                "client_lat": lat,
                "client_lng": lng,
                "radius_km": radius_km
            }
        ).execute()
        return [self.model_class(**item) for item in response.data]

    def get_active_offers_by_business(self, business_id: int) -> List[OffersEntity]:
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("business_id", business_id)
            .eq("status", "active")
            .gt("quantity_available", 0)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]
