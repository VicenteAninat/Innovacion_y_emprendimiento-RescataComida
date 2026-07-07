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

    def get_by_user_id(self, user_id: str) -> List[ReservationsEntity]:
        """Fetches reservations created by a specific user, including the associated offer.

        Args:
            user_id (str): UUID string of the customer.

        Returns:
            List[ReservationsEntity]: A list of reservations with offer details loaded.
        """
        # Carga la reserva e incluye los datos de la oferta asociada
        response = (
            supabase.table(self.table_name)
            .select("*, offer(*)")
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
        # Obtiene las reservas buscando a través del business_id de la oferta
        response = (
            supabase.table(self.table_name)
            .select("*, offer!inner(*)")
            .eq("offer.business_id", business_id)
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
            .select("*, offer(*)")
            .eq("id", id_val)
            .execute()
        )
        if not response.data:
            return None
        return response.data[0]
