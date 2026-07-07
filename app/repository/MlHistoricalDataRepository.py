"""ML Historical Data Repository.

This module defines the MlHistoricalDataRepository class which extends BaseRepository to fetch historical data for ML.
"""

from typing import List
from app.entity.MlHistoricalDataEntity import MlHistoricalDataEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class MlHistoricalDataRepository(BaseRepository[MlHistoricalDataEntity]):
    """Repository class managing database operations on the 'ml_historical_data' table."""

    def __init__(self):
        """Initializes the repository targeting the 'ml_historical_data' table."""
        super().__init__(MlHistoricalDataEntity, "ml_historical_data")

    def get_by_business_id(self, business_id: int) -> List[MlHistoricalDataEntity]:
        """Fetches ML historical records matching a specific business ID.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[MlHistoricalDataEntity]: List of historical records.
        """
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]
