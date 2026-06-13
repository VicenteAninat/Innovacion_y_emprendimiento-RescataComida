from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .UserEntity import UserEntity
    from .OffersEntity import OffersEntity
    from .ReviewsEntity import ReviewsEntity
    from .MlHistoricalDataEntity import MlHistoricalDataEntity
    from .DonationsEntity import DonationsEntity

class BusinessesEntity(BaseModel):
    id: Optional[int] = None
    rut: str
    name: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    is_premium: bool = False
    created_at: Optional[datetime] = None

    # Fields for joined relations
    users: Optional[List[UserEntity]] = None
    offers: Optional[List[OffersEntity]] = None
    reviews: Optional[List[ReviewsEntity]] = None
    ml_historical_data: Optional[List[MlHistoricalDataEntity]] = None
    donations: Optional[List[DonationsEntity]] = None
    favorited_by_users: Optional[List[UserEntity]] = None
