"""Reservations Entity.

This module defines the database representation schema for reservations made by customers.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .UserEntity import UserEntity
    from .OffersEntity import OffersEntity
    from .ReviewsEntity import ReviewsEntity

class ReservationsEntity(BaseModel):
    """Represents a reservation of an offer in the system.

    Attributes:
        id (Optional[int]): Unique identifier for the reservation.
        user_id (str): UUID identifier of the reserving user.
        offer_id (int): Foreign key referring to the associated offer.
        quantity (int): Number of units reserved. Defaults to 1.
        total_price (float): Total price of the reservation (quantity * discounted_price).
        status (str): Current status of reservation (pending, completed, cancelled). Defaults to "pending".
        payment_method (Optional[str]): Method of payment.
        transaction_fee (Optional[float]): Processing fee.
        created_at (Optional[datetime]): Timestamp when the reservation was created.
        user (Optional[UserEntity]): The user who made the reservation.
        offer (Optional[OffersEntity]): The offer reserved.
        review (Optional[ReviewsEntity]): The associated review, if any.
    """
    id: Optional[int] = None
    user_id: str
    offer_id: int
    quantity: int = 1
    total_price: float
    status: str = "pending"
    payment_method: Optional[str] = None
    transaction_fee: Optional[float] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    user: Optional[UserEntity] = None
    offer: Optional[OffersEntity] = None
    review: Optional[ReviewsEntity] = None
