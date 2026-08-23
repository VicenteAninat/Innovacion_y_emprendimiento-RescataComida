"""Offers Repository.

This module defines the OffersRepository class which extends BaseRepository to retrieve food bag offers from database.
"""

from typing import List
from app.entity.OffersEntity import OffersEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class OffersRepository(BaseRepository[OffersEntity]):
    """Repository class managing database operations on the 'offers' table."""

    def __init__(self):
        """Initializes the repository targeting the 'offers' table."""
        super().__init__(OffersEntity, "offers")

    @staticmethod
    def _attach_businesses(items: List[dict]) -> List[dict]:
        """Adjunta los datos del comercio a cada oferta (join manual).

        PostgREST no puede resolver `business(*)` cuando la BD no declara
        foreign keys, así que se buscan los comercios por separado.
        """
        if not items:
            return items
        business_ids = list({item["business_id"] for item in items if item.get("business_id") is not None})
        if not business_ids:
            return items
        response = (
            supabase.table("businesses")
            .select("*")
            .in_("id", business_ids)
            .execute()
        )
        by_id = {b["id"]: b for b in response.data}
        for item in items:
            item["business"] = by_id.get(item.get("business_id"))
        return items

    def get_active_offers(self) -> List[OffersEntity]:
        """Fetches all active offers that have stock greater than 0, including business details.

        Returns:
            List[OffersEntity]: List of active offers.
        """
        # Lista ofertas con estado 'active' y cantidad disponible mayor a 0
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("status", "active")
            .gt("quantity_available", 0)
            .execute()
        )
        return [self.model_class(**item) for item in self._attach_businesses(response.data)]

    def get_offers_by_business(self, business_id: int) -> List[OffersEntity]:
        """Fetches all offers (active or inactive) created by a given business ID.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[OffersEntity]: List of all offers for the business.
        """
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_favorite_businesses_offers_nearby(self, user_id: str, lat: float, lng: float, radius_km: float = 5.0) -> List[OffersEntity]:
        """Calls PostgreSQL RPC to locate nearby active offers from favorite businesses.

        Args:
            user_id (str): UUID string of the customer.
            lat (float): Latitude coordinate.
            lng (float): Longitude coordinate.
            radius_km (float): Search radius in kilometers. Defaults to 5.0.

        Returns:
            List[OffersEntity]: List of active offers in range.
        """
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
        """Fetches only active, in-stock offers for a single business.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[OffersEntity]: List of active in-stock offers for the business.
        """
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("business_id", business_id)
            .eq("status", "active")
            .gt("quantity_available", 0)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_active_offers_paginated(self, limit: int = 10, offset: int = 0) -> List[OffersEntity]:
        """Fetches active, in-stock offers globally, using range pagination.

        Args:
            limit (int): Max number of records to return. Defaults to 10.
            offset (int): Offset of records to skip. Defaults to 0.

        Returns:
            List[OffersEntity]: List of active offers.
        """
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("status", "active")
            .gt("quantity_available", 0)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return [self.model_class(**item) for item in self._attach_businesses(response.data)]

    def get_active_offers_nearby(self, lat: float, lng: float, radius_km: float = 5.0, limit: int = 10, offset: int = 0) -> List[OffersEntity]:
        """Calls PostgreSQL RPC to locate nearby active offers, sorted by distance.

        Args:
            lat (float): Latitude coordinate of client.
            lng (float): Longitude coordinate of client.
            radius_km (float): Search radius in kilometers. Defaults to 5.0.
            limit (int): Max number of records. Defaults to 10.
            offset (int): Skip count. Defaults to 0.

        Returns:
            List[OffersEntity]: List of active offers in range, ordered by distance.
        """
        response = supabase.rpc(
            "get_active_offers_nearby",
            {
                "client_lat": lat,
                "client_lng": lng,
                "radius_km": radius_km,
                "limit_val": limit,
                "offset_val": offset
            }
        ).execute()
        return [self.model_class(**item) for item in response.data]
