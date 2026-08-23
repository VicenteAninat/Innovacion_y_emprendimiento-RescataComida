"""User Repository.

This module defines the UserRepository class which extends BaseRepository to manage user profiles in the database.
"""

from typing import Optional
from app.entity.UserEntity import UserEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class UserRepository(BaseRepository[UserEntity]):
    """Repository class managing database operations on the 'users' table."""

    def __init__(self):
        """Initializes the repository targeting the 'users' table."""
        super().__init__(UserEntity, "users")

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Fetches a user profile by email address.

        Args:
            email (str): The email address to look up.

        Returns:
            Optional[UserEntity]: The user entity if found, otherwise None.
        """
        response = supabase.table(self.table_name).select("*").eq("email", email).execute()
        if not response.data:
            return None
        return self.model_class(**response.data[0])

    def get_user_with_business(self, user_id: str) -> Optional[UserEntity]:
        """Fetches user details along with the nested associated business, if any.

        Args:
            user_id (str): UUID string of the user.

        Returns:
            Optional[UserEntity]: The user entity with business details if found, otherwise None.
        """
        # Join manual: la BD no declara FKs, se busca el comercio por separado
        response = supabase.table(self.table_name).select("*").eq("id", user_id).execute()
        if not response.data:
            return None
        item = response.data[0]
        if item.get("business_id") is not None:
            business_response = (
                supabase.table("businesses")
                .select("*")
                .eq("id", item["business_id"])
                .execute()
            )
            item["business"] = business_response.data[0] if business_response.data else None
        return self.model_class(**item)
