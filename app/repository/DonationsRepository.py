"""Donations Repository.

This module defines the DonationsRepository class which extends BaseRepository to offer specialized queries for donations.
"""

from typing import List
from app.entity.DonationsEntity import DonationsEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class DonationsRepository(BaseRepository[DonationsEntity]):
    """Repository class managing database operations on the 'donations' table."""

    def __init__(self):
        """Initializes the repository targeting the 'donations' table."""
        super().__init__(DonationsEntity, "donations")

    def get_by_business_id(self, business_id: int) -> List[DonationsEntity]:
        """Fetches all donation records for a specific business, including associated food bank details.

        Args:
            business_id (int): ID of the business.

        Returns:
            List[DonationsEntity]: A list of donation records.
        """
        # Carga la donación con el banco de alimentos asociado
        response = (
            supabase.table(self.table_name)
            .select("*, food_bank(*)")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]
