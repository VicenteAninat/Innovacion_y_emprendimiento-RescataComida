from typing import List, Optional
from app.entity.BusinessesEntity import BusinessesEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class BusinessesRepository(BaseRepository[BusinessesEntity]):
    def __init__(self):
        super().__init__(BusinessesEntity, "businesses")

    def get_nearby_businesses_with_active_offers(self, lat: float, lng: float, radius_km: float = 5.0) -> List[BusinessesEntity]:
        # Las consultas de geolocalización complejas (PostGIS) con REST se realizan llamando a una función RPC de PostgreSQL
        response = supabase.rpc(
            "get_nearby_businesses_with_active_offers", 
            {"client_lat": lat, "client_lng": lng, "radius_km": radius_km}
        ).execute()
        return [self.model_class(**item) for item in response.data]

    def get_businesses_with_active_offers(self) -> List[BusinessesEntity]:
        # Retorna los comercios cargando sus ofertas anidadas filtrando por estado activo
        # Nota: La sintaxis de PostgREST para joins anidados condicionales es select("*, offers(...)")
        response = supabase.table(self.table_name).select("*, offers(*)").eq("offers.status", "active").execute()
        # Filtrar comercios que al menos tengan 1 oferta activa
        result = []
        for item in response.data:
            if item.get("offers"):
                result.append(self.model_class(**item))
        return result

    def get_favorite_businesses_with_active_offers_nearby(self, user_id: str, lat: float, lng: float, radius_km: float = 5.0) -> List[BusinessesEntity]:
        response = supabase.rpc(
            "get_favorite_businesses_with_active_offers_nearby",
            {
                "client_user_id": user_id,
                "client_lat": lat,
                "client_lng": lng,
                "radius_km": radius_km
            }
        ).execute()
        return [self.model_class(**item) for item in response.data]
