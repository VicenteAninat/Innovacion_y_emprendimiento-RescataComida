"""User Favorites Service.

This module defines the UserFavoritesService class which handles business logic for managing user favorite businesses.
"""

from typing import List
from app.entity.UserFavoritesEntity import UserFavoritesEntity
from app.entity.BusinessesEntity import BusinessesEntity
from app.repository.UserFavoritesRepository import UserFavoritesRepository

class UserFavoritesService:
    """Service class encapsulating favorite business list operations."""

    def __init__(self):
        """Initializes the service by setting up the UserFavoritesRepository."""
        self.user_favorites_repository = UserFavoritesRepository()

    def add_favorite(self, user_id: str, business_id: int) -> UserFavoritesEntity:
        """Adds a business to the user's favorites list.

        Args:
            user_id (str): UUID string of the customer.
            business_id (int): Unique identifier of the business.

        Returns:
            UserFavoritesEntity: The user favorite mapping record created.
        """
        return self.user_favorites_repository.add_favorite(user_id, business_id)

    def remove_favorite(self, user_id: str, business_id: int) -> bool:
        """Removes a business from the user's favorites list.

        Args:
            user_id (str): UUID string of the customer.
            business_id (int): Unique identifier of the business.

        Returns:
            bool: True if favorite was successfully removed, False otherwise.
        """
        return self.user_favorites_repository.remove_favorite(user_id, business_id)

    def is_favorite(self, user_id: str, business_id: int) -> bool:
        """Checks if a business is currently favorited by a user.

        Args:
            user_id (str): UUID string of the customer.
            business_id (int): Unique identifier of the business.

        Returns:
            bool: True if it is a favorite, False otherwise.
        """
        return self.user_favorites_repository.is_favorite(user_id, business_id)

    def get_favorites_by_user(self, user_id: str) -> List[BusinessesEntity]:
        """Retrieves all businesses that are favorited by a user.

        Args:
            user_id (str): UUID string of the customer.

        Returns:
            List[BusinessesEntity]: List of favorited business entities.
        """
        return self.user_favorites_repository.get_favorites_by_user(user_id)
