"""Reviews Entity.

This module defines the database representation schema for customer reviews.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .UserEntity import UserEntity
    from .BusinessesEntity import BusinessesEntity
    from .ReservationsEntity import ReservationsEntity

class ReviewsEntity(BaseModel):
    """Represents a customer review/rating in the system.

    Attributes:
        id (Optional[int]): Unique identifier for the review.
        user_id (str): UUID identifier of the reviewing user.
        business_id (int): Foreign key referring to the associated business.
        reservation_id (int): Foreign key referring to the reservation being reviewed.
        rating (int): Star rating (1-5).
        comment (Optional[str]): Text review comment.
        created_at (Optional[datetime]): Timestamp when the review was created.
        user (Optional[UserEntity]): The user who wrote the review.
        business (Optional[BusinessesEntity]): The business that was reviewed.
        reservation (Optional[ReservationsEntity]): The associated reservation.
    """
    id: Optional[int] = None
    user_id: str
    business_id: int
    reservation_id: int
    rating: int
    comment: Optional[str] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    user: Optional[UserEntity] = None
    business: Optional[BusinessesEntity] = None
    reservation: Optional[ReservationsEntity] = None
