from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity
    from .ReservationsEntity import ReservationsEntity

class OffersEntity(BaseModel):
    id: Optional[int] = None
    business_id: int
    title: str
    description: Optional[str] = None
    original_price: float
    discounted_price: float
    quantity_available: int = 1
    pickup_start_time: datetime
    pickup_end_time: datetime
    status: str = "active"
    kg_saved_per_unit: Optional[float] = None
    co2_avoided_per_unit: Optional[float] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    business: Optional[BusinessesEntity] = None
    reservations: Optional[List[ReservationsEntity]] = None
