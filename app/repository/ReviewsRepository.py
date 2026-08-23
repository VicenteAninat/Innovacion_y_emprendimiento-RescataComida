"""Reviews Repository.

This module defines the ReviewsRepository class which extends BaseRepository to retrieve customer reviews.
"""

from typing import List
from app.entity.ReviewsEntity import ReviewsEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class ReviewsRepository(BaseRepository[ReviewsEntity]):
    """Repository class managing database operations on the 'reviews' table."""

    def __init__(self):
        """Initializes the repository targeting the 'reviews' table."""
        super().__init__(ReviewsEntity, "reviews")

    def get_by_business_id(self, business_id: int) -> List[ReviewsEntity]:
        """Fetches reviews associated with a business.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[ReviewsEntity]: List of reviews.
        """
        # Sin embed de user(*) porque la BD no declara FKs (PostgREST PGRST200)
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]
