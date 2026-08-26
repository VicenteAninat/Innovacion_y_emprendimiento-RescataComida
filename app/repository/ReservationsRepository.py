"""Reservations Repository.

This module defines the ReservationsRepository class which extends BaseRepository to retrieve customer reservation details.
"""

from typing import List, Optional
from app.entity.ReservationsEntity import ReservationsEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class ReservationsRepository(BaseRepository[ReservationsEntity]):
    """Repository class managing database operations on the 'reservations' table."""

    def __init__(self):
        """Initializes the repository targeting the 'reservations' table."""
        super().__init__(ReservationsEntity, "reservations")

    def get_all(self) -> List[ReservationsEntity]:
        """Fetches all reservations with manual join for users."""
        response = supabase.table(self.table_name).select("*").execute()
        items = response.data
        if not items:
            return []
            
        user_ids = list(set(item.get("user_id") for item in items if item.get("user_id")))
        users_map = {}
        if user_ids:
            users_response = supabase.table("users").select("*").in_("id", user_ids).execute()
            if users_response.data:
                for u in users_response.data:
                    users_map[u["id"]] = u
                    
        for item in items:
            uid = item.get("user_id")
            if uid and uid in users_map:
                item["user"] = users_map[uid]
                
        return [self.model_class(**item) for item in items]

    def get_by_user_id(self, user_id: str) -> List[ReservationsEntity]:
        """Fetches reservations created by a specific user.

        Args:
            user_id (str): UUID string of the customer.

        Returns:
            List[ReservationsEntity]: A list of reservations.
        """
        # Sin embed de offer(*) porque la BD no declara FKs (PostgREST PGRST200)
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_by_business_id(self, business_id: int) -> List[ReservationsEntity]:
        """Fetches reservations of offers belonging to a specific business.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[ReservationsEntity]: A list of reservations belonging to the business.
        """
        # Join manual: primero las ofertas del comercio, luego sus reservas
        offers_response = (
            supabase.table("offers")
            .select("id")
            .eq("business_id", business_id)
            .execute()
        )
        offer_ids = [o["id"] for o in offers_response.data]
        if not offer_ids:
            return []
        response = (
            supabase.table(self.table_name)
            .select("*")
            .in_("offer_id", offer_ids)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_reservation_with_offer(self, id_val: int) -> Optional[dict]:
        """Fetches a reservation with nested offer details as a dictionary.

        Args:
            id_val (int): ID of the reservation record.

        Returns:
            Optional[dict]: Dictionary with reservation and offer details, or None if not found.
        """
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("id", id_val)
            .execute()
        )
        if not response.data:
            return None
        item = response.data[0]
        # Join manual: la oferta se busca por separado
        offer_response = (
            supabase.table("offers")
            .select("*")
            .eq("id", item.get("offer_id"))
            .execute()
        )
        item["offer"] = offer_response.data[0] if offer_response.data else None
        return item
