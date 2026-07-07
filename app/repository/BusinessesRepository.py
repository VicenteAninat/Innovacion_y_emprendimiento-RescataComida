"""Businesses Repository.

This module defines the BusinessesRepository class which extends BaseRepository to offer specialized database queries for businesses,
such as nearby geolocation and favorites filtering with active offers.
"""

from typing import List, Optional
from app.entity.BusinessesEntity import BusinessesEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class BusinessesRepository(BaseRepository[BusinessesEntity]):
    """Repository class managing database operations on the 'businesses' table."""

    def __init__(self):
        """Initializes the repository targeting the 'businesses' table."""
        super().__init__(BusinessesEntity, "businesses")

    def get_nearby_businesses_with_active_offers(self, lat: float, lng: float, radius_km: float = 5.0) -> List[BusinessesEntity]:
        """Calls a PostgreSQL RPC function to find nearby businesses with active offers using PostGIS.

        Args:
            lat (float): The latitude of the search center point.
            lng (float): The longitude of the search center point.
            radius_km (float): The radius in kilometers. Defaults to 5.0.

        Returns:
            List[BusinessesEntity]: A list of businesses within the specified radius that have active offers.
        """
        # Las consultas de geolocalización complejas (PostGIS) con REST se realizan llamando a una función RPC de PostgreSQL
        response = supabase.rpc(
            "get_nearby_businesses_with_active_offers", 
            {"client_lat": lat, "client_lng": lng, "radius_km": radius_km}
        ).execute()
        return [self.model_class(**item) for item in response.data]

    def get_businesses_with_active_offers(self) -> List[BusinessesEntity]:
        """Fetches all businesses that have at least one active offer associated.

        Returns:
            List[BusinessesEntity]: A list of businesses with their active offers loaded.
        """
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
        """Calls a PostgreSQL RPC function to find nearby favorite businesses with active offers.

        Args:
            user_id (str): UUID string of the customer.
            lat (float): Latitude of search center.
            lng (float): Longitude of search center.
            radius_km (float): Search radius in kilometers. Defaults to 5.0.

        Returns:
            List[BusinessesEntity]: A list of favorite businesses in range with active offers.
        """
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
