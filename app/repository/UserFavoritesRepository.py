"""User Favorites Repository.

This module defines the UserFavoritesRepository class which extends BaseRepository to manage customer's favorite business lists.
"""

from typing import List, Optional
from app.entity.UserFavoritesEntity import UserFavoritesEntity
from app.entity.BusinessesEntity import BusinessesEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class UserFavoritesRepository(BaseRepository[UserFavoritesEntity]):
    """Repository class managing database operations on the 'user_favorites' table."""

    def __init__(self):
        """Initializes the repository targeting the 'user_favorites' table."""
        super().__init__(UserFavoritesEntity, "user_favorites")

    def add_favorite(self, user_id: str, business_id: int) -> UserFavoritesEntity:
        """Associates a business to a user's favorite list.

        Args:
            user_id (str): UUID string of the user.
            business_id (int): Unique identifier of the business.

        Returns:
            UserFavoritesEntity: The created user favorite mapping record.
        """
        entity = UserFavoritesEntity(user_id=user_id, business_id=business_id)
        return self.create(entity)

    def remove_favorite(self, user_id: str, business_id: int) -> bool:
        """Disassociates a business from a user's favorite list.

        Args:
            user_id (str): UUID string of the user.
            business_id (int): Unique identifier of the business.

        Returns:
            bool: True if favorite was removed, False otherwise.
        """
        response = (
            supabase.table(self.table_name)
            .delete()
            .eq("user_id", user_id)
            .eq("business_id", business_id)
            .execute()
        )
        return len(response.data) > 0

    def is_favorite(self, user_id: str, business_id: int) -> bool:
        """Checks if a business is currently marked as favorite by a specific user.

        Args:
            user_id (str): UUID string of the user.
            business_id (int): Unique identifier of the business.

        Returns:
            bool: True if it is a favorite, False otherwise.
        """
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("user_id", user_id)
            .eq("business_id", business_id)
            .execute()
        )
        return len(response.data) > 0

    def get_favorites_by_user(self, user_id: str) -> List[BusinessesEntity]:
        """Retrieves a list of businesses marked as favorites by a user.

        Args:
            user_id (str): UUID string of the user.

        Returns:
            List[BusinessesEntity]: List of businesses marked as favorites.
        """
        # Join manual: primero los ids de favoritos, luego los comercios
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        business_ids = list({item["business_id"] for item in response.data})
        if not business_ids:
            return []
        businesses_response = (
            supabase.table("businesses")
            .select("*")
            .in_("id", business_ids)
            .execute()
        )
        return [BusinessesEntity(**item) for item in businesses_response.data]
