"""User Favorites Entity.

This module defines the database representation schema for users' favorite businesses mapping.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserFavoritesEntity(BaseModel):
    """Represents a favorite business mapping for a user in the system.

    Attributes:
        user_id (str): UUID identifier of the user.
        business_id (int): Foreign key identifier of the business.
        created_at (Optional[datetime]): Timestamp when the business was favorited.
    """
    user_id: str
    business_id: int
    created_at: Optional[datetime] = None
