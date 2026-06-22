from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .UserEntity import UserEntity
    from .BusinessesEntity import BusinessesEntity
    from .ReservationsEntity import ReservationsEntity

class ReviewsEntity(BaseModel):
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
