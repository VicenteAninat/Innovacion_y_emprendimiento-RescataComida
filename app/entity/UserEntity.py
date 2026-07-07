"""User Entity.

This module defines the database representation schema for users (customers, workers, admins).
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity
    from .ReservationsEntity import ReservationsEntity
    from .ReviewsEntity import ReviewsEntity

class UserEntity(BaseModel):
    """Represents a user in the system.

    Attributes:
        id (Optional[str]): Unique UUID string identifier of the user.
        name (Optional[str]): Full name of the user.
        email (str): Email address of the user.
        phone (Optional[str]): Phone number of the user.
        role (str): Role within the system (customer, worker, admin). Defaults to "customer".
        business_id (Optional[int]): ID of the business if user role is worker.
        created_at (Optional[datetime]): Timestamp when user profile was created.
        business (Optional[BusinessesEntity]): Related business, if worker.
        reservations (Optional[List[ReservationsEntity]]): User's reservations.
        reviews (Optional[List[ReviewsEntity]]): Reviews written by this user.
        favorite_businesses (Optional[List[BusinessesEntity]]): User's favorite businesses.
    """
    id: Optional[str] = None
    name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    role: str = "customer"
    business_id: Optional[int] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    business: Optional[BusinessesEntity] = None
    reservations: Optional[List[ReservationsEntity]] = None
    reviews: Optional[List[ReviewsEntity]] = None
    favorite_businesses: Optional[List[BusinessesEntity]] = None
