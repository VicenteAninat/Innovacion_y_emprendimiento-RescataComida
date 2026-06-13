from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .UserEntity import UserEntity
    from .OffersEntity import OffersEntity
    from .ReviewsEntity import ReviewsEntity

class ReservationsEntity(BaseModel):
    id: Optional[int] = None
    user_id: int
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
