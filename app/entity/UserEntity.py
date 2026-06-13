from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity
    from .ReservationsEntity import ReservationsEntity
    from .ReviewsEntity import ReviewsEntity

class UserEntity(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: str
    password_hash: Optional[str] = None
    phone: Optional[str] = None
    role: str = "customer"
    business_id: Optional[int] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    business: Optional[BusinessesEntity] = None
    reservations: Optional[List[ReservationsEntity]] = None
    reviews: Optional[List[ReviewsEntity]] = None
    favorite_businesses: Optional[List[BusinessesEntity]] = None
